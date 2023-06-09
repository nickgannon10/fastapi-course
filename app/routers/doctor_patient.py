from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, database
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from .. import models, schemas, database, oauth2

router = APIRouter(tags=['DoctorPatient'])

async def get_current_doctor_or_superuser(current_user: schemas.UserCreate = Depends(oauth2.get_current_user)):
    if current_user.user_type not in ["DOCTOR", "SUPERUSER"]:
        raise HTTPException(
            status_code=400, detail="The user does not have the right privileges"
        )
    return current_user

async def get_current_patient_or_superuser(current_user: schemas.UserCreate = Depends(oauth2.get_current_user)):
    if current_user.user_type not in ["PATIENT", "SUPERUSER"]:
        raise HTTPException(
            status_code=400, detail="The user does not have the right privileges"
        )
    return current_user

@router.post('/doctor_requests/', status_code=status.HTTP_201_CREATED)
def create_doctor_request(patient_id: int, db: Session = Depends(database.get_db),
                          current_user: schemas.UserCreate = Depends(get_current_doctor_or_superuser)):
    # Ensuring that the current user is a doctor
    doctor = db.query(models.Doctor).filter(models.Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not a doctor"
        )
    # Check if the patient exists in the system
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    # Check if doctor already requested this patient
    doctor_request = db.query(models.DoctorRequest).filter(
        models.DoctorRequest.patient_id == patient_id,
        models.DoctorRequest.doctor_id == doctor.id,
    ).first()

    if doctor_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor has already sent a request to this patient"
        )

    # Create the doctor's request
    doctor_request = models.DoctorRequest(doctor_id=doctor.id, patient_id=patient_id)
    db.add(doctor_request)
    db.commit()

    return {"detail": "Doctor's request to Patient has been created successfully"}

@router.post('/patient_requests/', status_code=status.HTTP_201_CREATED)
def create_patient_request(doctor_id: int, db: Session = Depends(database.get_db),
                           current_patient: schemas.UserCreate = Depends(get_current_patient_or_superuser)):
    if not current_patient.patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    # Check if patient already requested this doctor
    patient_request = db.query(models.PatientRequest).filter(
        models.PatientRequest.doctor_id == doctor_id,
        models.PatientRequest.patient_id == current_patient.patient.id,
    ).first()

    if patient_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient has already sent a request to this doctor"
        )

    # Create the patient's request
    patient_request = models.PatientRequest(doctor_id=doctor_id, patient_id=current_patient.patient.id)
    db.add(patient_request)
    db.commit()

    return {"detail": "Patient's request to Doctor has been created successfully"}

@router.post('/doctor_patient/', status_code=status.HTTP_201_CREATED)
def create_doctor_patient(patient_id: int, doctor_id: int, db: Session = Depends(database.get_db),
                          current_doctor: schemas.UserCreate = Depends(get_current_doctor_or_superuser)):
    # Check doctor_request table for acceptance status
    doctor_request = db.query(models.DoctorRequest).filter(
        models.DoctorRequest.patient_id == patient_id,
        models.DoctorRequest.doctor_id == doctor_id,
        models.DoctorRequest.ACCEPTED == "Accepted"
    ).first()

    if not doctor_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor has not accepted the request from this patient"
        )

    # Check patient_request table for acceptance status
    patient_request = db.query(models.PatientRequest).filter(
        models.PatientRequest.doctor_id == doctor_id,
        models.PatientRequest.patient_id == patient_id,
        models.PatientRequest.ACCEPTED == "Accepted"
    ).first()

    if not patient_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient has not accepted the request from this doctor"
        )

    # Create the doctor-patient relationship
    doctor_patient_relationship = models.DoctorPatient(doctor_id=doctor_id, patient_id=patient_id)
    db.add(doctor_patient_relationship)
    db.commit()

    return {"detail": "Doctor-Patient relationship created successfully"}
