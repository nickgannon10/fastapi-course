from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from enum import Enum

from .database import Base

class UserType(str, Enum):
    DOCTOR = "Doctor"
    PATIENT = "Patient"

class RequestStatus(str, Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"

# Define association tables for many-to-many relationships
doctor_patient_table = Table('doctor_patient', Base.metadata,
    Column('doctor_id', Integer, ForeignKey('doctors.id', ondelete="CASCADE")),
    Column('patient_id', Integer, ForeignKey('patients.id', ondelete="CASCADE"))
)

doctor_specialty_table = Table('doctor_specialty', Base.metadata,
    Column('doctor_id', Integer, ForeignKey('doctors.id', ondelete="CASCADE")),
    Column('specialty_id', Integer, ForeignKey('specialties.id', ondelete="CASCADE"))
)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_type = Column(SQLEnum(UserType)) 
    is_superuser = Column(Boolean, default=False, nullable=False)
    doctor = relationship("Doctor", back_populates="user")
    patient = relationship("Patient", back_populates="user")



class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
    
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    degree = Column(String, nullable=False)
    user = relationship("User", back_populates="doctor")
    doctor_requests = relationship("DoctorRequest", back_populates="doctor")
    patient_requests = relationship("PatientRequest", back_populates="doctor")


    # define relationship to patients through Doctor_Patient table
    patients = relationship("Patient", secondary=doctor_patient_table, back_populates="doctors")

    # define relationship to specialties through Doctor_Specialty table
    specialties = relationship("Specialty", secondary=doctor_specialty_table, back_populates="doctors")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="patient")
    doctor_requests = relationship("DoctorRequest", back_populates="patient")
    patient_requests = relationship("PatientRequest", back_populates="patient")

    # define relationship to doctors through Doctor_Patient table
    doctors = relationship("Doctor", secondary=doctor_patient_table, back_populates="patients")


class Specialty(Base):
    __tablename__ = "specialties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # define relationship to doctors through Doctor_Specialty table
    doctors = relationship("Doctor", secondary=doctor_specialty_table, back_populates="specialties")

class LanguageModel(Base):
    __tablename__ = "language_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class DoctorRequest(Base):
    __tablename__ = "doctor_requests"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id', ondelete="CASCADE"))
    patient_id = Column(Integer, ForeignKey('patients.id', ondelete="CASCADE"))
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.PENDING)

    doctor = relationship("Doctor", back_populates="doctor_requests")
    patient = relationship("Patient", back_populates="doctor_requests")

class PatientRequest(Base):
    __tablename__ = "patient_requests"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id', ondelete="CASCADE"))
    patient_id = Column(Integer, ForeignKey('patients.id', ondelete="CASCADE"))
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.PENDING)

    doctor = relationship("Doctor", back_populates="patient_requests")
    patient = relationship("Patient", back_populates="patient_requests")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String) #server_default=text('Health Inquiry'))
    description = Column(String, nullable=False)
    creation_date = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship("Patient")

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    creation_date = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    llm_id = Column(Integer, ForeignKey('language_models.id'))
    question = relationship("Question")
    language_model = relationship("LanguageModel")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    creation_date = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=True)
    answer_id = Column(Integer, ForeignKey('answers.id'), nullable=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=True)
    doctor = relationship("Doctor")
    question = relationship("Question")
    answer = relationship("Answer")
