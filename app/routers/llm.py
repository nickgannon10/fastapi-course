from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from .. import models, schemas, database, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/language_models",
    tags=['Language Models']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.LanguageModel)
async def create_language_model(language_model: schemas.LanguageModelCreate,
                                db: Session = Depends(get_db),
                                current_user: models.User = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    new_language_model = models.LanguageModel(**language_model.dict())
    db.add(new_language_model)
    db.commit()
    db.refresh(new_language_model)

    return new_language_model

@router.get("/", response_model=List[schemas.LanguageModel])
async def read_all_language_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    language_models = db.query(models.LanguageModel).offset(skip).limit(limit).all()
    return language_models

# from fastapi import APIRouter, Depends, HTTPException, status, Security
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# from jose import JWTError, jwt
# from .. import models, schemas, database, oauth2
# from ..database import get_db
# from typing import List

# # This will get the token from the request header
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# router = APIRouter(
#     prefix="/language_models",
#     tags=['Language Models']
# )

# async def get_current_user_id(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#     )
#     try:
#         payload = jwt.decode(token, oauth2.SECRET_KEY, algorithms=[oauth2.ALGORITHM])
#         user_id: str = payload.get("user_id")
#         if user_id is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     return user_id

# # MAKE SURE TO IMPLMENET the router in main.py

# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.LanguageModel)
# async def create_language_model(language_model: schemas.LanguageModelCreate,
#                                 db: Session = Depends(get_db),
#                                 current_user_id: int = Depends(get_current_user_id)):
#     user = db.query(models.User).filter(models.User.id == current_user_id).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if not user.is_superuser:
#         raise HTTPException(status_code=403, detail="Not enough permissions")

#     new_language_model = models.LanguageModel(**language_model.dict())
#     db.add(new_language_model)
#     db.commit()
#     db.refresh(new_language_model)

#     return new_language_model

# @router.get("/", response_model=List[schemas.LanguageModel])
# async def read_all_language_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     language_models = db.query(models.LanguageModel).offset(skip).limit(limit).all()
#     return language_models


