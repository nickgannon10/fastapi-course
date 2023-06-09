from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..schemas import UserType
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)
# /users/
# /users

### ------------------ Posts ------------------ ###
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/doctors", status_code=status.HTTP_201_CREATED, response_model=schemas.DoctorOut)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == doctor.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {doctor.user_id} does not exist")

    if user.user_type != UserType.DOCTOR:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User type is not Doctor")

    new_doctor = models.Doctor(**doctor.dict())
    try: 
        db.add(new_doctor)
        db.commit()
        db.refresh(new_doctor)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return new_doctor


@router.post("/patients", status_code=status.HTTP_201_CREATED, response_model=schemas.PatientOut)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == patient.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {patient.user_id} does not exist")

    if user.user_type != UserType.PATIENT:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User type is not Patient")

    new_patient = models.Patient(**patient.dict())
    try: 
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return new_patient

### ------------------ Get ------------------ ###
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user
