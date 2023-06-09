from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

from enum import Enum

class UserType(str, Enum):
    DOCTOR = "Doctor"
    PATIENT = "Patient"

class RequestStatus(str, Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    user_type: UserType 


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

### ------------------ Doctor ------------------ ###
class DoctorBase(BaseModel):
    user_id: int
    degree: str

class DoctorCreate(DoctorBase):
    pass

class DoctorOut(DoctorBase):
    id: int

    class Config:
        orm_mode = True

### ------------------ Patient ------------------ ###
class PatientBase(BaseModel):
    user_id: int

class PatientCreate(PatientBase):
    pass

class PatientOut(PatientBase):
    id: int

    class Config:
        orm_mode = True

### ------------------ Patient-Doctor ------------------ ###
class DoctorRequestBase(BaseModel):
    doctor_id: int
    patient_id: int
    status: RequestStatus = RequestStatus.PENDING

class DoctorRequestCreate(DoctorRequestBase):
    pass

class DoctorRequest(DoctorRequestBase):
    id: int

    class Config:
        orm_mode = True

class PatientRequestBase(BaseModel):
    doctor_id: int
    patient_id: int
    status: RequestStatus = RequestStatus.PENDING

class PatientRequestCreate(PatientRequestBase):
    pass

class PatientRequest(PatientRequestBase):
    id: int

    class Config:
        orm_mode = True


### ------------------ Specialty ------------------ ###
class SpecialtyBase(BaseModel):
    name: str

class SpecialtyCreate(SpecialtyBase):
    pass

class Specialty(SpecialtyBase):
    id: int

    class Config:
        orm_mode = True

### ------------------ LLM ------------------ ###
class LanguageModelBase(BaseModel):
    name: str

class LanguageModelCreate(LanguageModelBase):
    pass

class LanguageModel(LanguageModelBase):
    id: int

    class Config:
        orm_mode = True

### ------------------ Question ------------------ ###
class QuestionBase(BaseModel):
    title: str
    description: str
    patient_id: int

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    creation_date: datetime

    class Config:
        orm_mode = True

### ------------------ Answer ------------------ ###
class AnswerBase(BaseModel):
    content: str
    question_id: int
    llm_id: int

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    creation_date: datetime

    class Config:
        orm_mode = True

### ------------------ Comment ------------------ ###
class CommentBase(BaseModel):
    content: str
    doctor_id: int
    question_id: Optional[int]
    answer_id: Optional[int]

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    creation_date: datetime

    class Config:
        orm_mode = True

