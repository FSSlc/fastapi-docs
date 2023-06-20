import uvicorn
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, HTTPException, status, Depends

app = FastAPI()


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AstronautModel(Base):
    __tablename__ = "astronauts"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    active = Column(Boolean, nullable=True)


class AstronautSchema(BaseModel):
    firstname: str
    lastname: str
    active: bool | None = True

    class Config:
        orm_mode = True


Base.metadata.create_all(engine)


@app.post("/astronaut", status_code=status.HTTP_201_CREATED)
def post(request: AstronautSchema, db: Session = Depends(get_db)):
    mark = AstronautModel(**request.dict())
    db.add(astro)
    db.commit()
    db.refresh(astro)
    return astro


@app.get("/astronaut", response_model=list[AstronautSchema])
def list_all(db: Session = Depends(get_db)):
    return db.query(AstronautModel).all()


@app.get(
    "/astronaut/{id}", status_code=status.HTTP_200_OK, response_model=AstronautSchema
)
def get(id: int, db: Session = Depends(get_db)):
    if result := db.query(AstronautModel).filter(AstronautModel.id == id).first():
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Astronaut does not exist"
        )


@app.delete("/astronaut/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    astro = db.query(AstronautModel).filter(AstronautModel.id == id)
    if not astro.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Astronaut does not exist"
        )
    astro.delete(synchronize_session=False)
    db.commit()


@app.put("/astronaut/{id}", status_code=status.HTTP_202_ACCEPTED)
def put(id: int, request: AstronautSchema, db: Session = Depends(get_db)):
    astro = db.query(AstronautModel).filter(AstronautModel.id == id)
    if not astro.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Astronaut does not exist"
        )
    astro.update(request)
    db.commit()
    return request


if __name__ == "__main__":
    uvicorn.run("test:app", host="127.0.0.1", port=8000, reload=True)
