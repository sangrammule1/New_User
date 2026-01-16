from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Define the database base
Base = declarative_base()


# Define the Entity model
class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Added name field for example


# Define the Landmark model
class Landmark(Base):
    __tablename__ = "landmarks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    entity_id = Column(Integer, nullable=False)


# Define the schemas
class EntityCreate(BaseModel):
    name: str = Field(..., description="Entity name")  # Required field example


class EntityUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Entity name")


class EntityResponse(BaseModel):
    id: int
    name: str


class EntityListResponse(BaseModel):
    entities: List[EntityResponse]


class LandmarkCreate(BaseModel):
    name: str = Field(..., description="Landmark name")
    description: Optional[str] = Field(None, description="Landmark description")
    latitude: float = Field(..., description="Landmark latitude")
    longitude: float = Field(..., description="Landmark longitude")
    entity_id: int = Field(..., description="Entity ID for the landmark")


class LandmarkUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Landmark name")
    description: Optional[str] = Field(None, description="Landmark description")
    latitude: Optional[float] = Field(None, description="Landmark latitude")
    longitude: Optional[float] = Field(None, description="Landmark longitude")
    entity_id: Optional[int] = Field(None, description="Entity ID for the landmark")


class LandmarkResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    latitude: float
    longitude: float
    entity_id: int


class LandmarkListResponse(BaseModel):
    landmarks: List[LandmarkResponse]


# Define the database session dependency
def get_db():
    
    Dummy database session for demonstration purposes.
    Replace with your actual database connection.
    
    # In a real application, you'd use a database engine and session factory
    # For example:
    # from sqlalchemy import create_engine, Session
    # engine = create_engine("sqlite:///./test.db")  # Replace with your database URL
    # LocalSession = sessionmaker(bind=engine)
    # db = LocalSession()
    # return db
    class MockSession:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def add(self, instance):
            self.mock_data.append(instance)
        def commit(self):
            pass
        def refresh(self, instance):
            pass
        def query(self, model):
            return MockQuery(self, model)

    return MockSession()


class MockQuery:
    def __init__(self, session, model):
        self.session = session
        self.model = model
        self.results = []

    def filter(self, *args):
        return self

    def first(self):
        if self.results:
            return self.results[0]
        else:
            return None

    def all(self):
        return self.results

    def add(self, instance):
        self.session.add(instance)

    def refresh(self, instance):
        self.session.refresh(instance)

    def __iter__(self):
        return iter(self.results)


# Create the router
router = APIRouter(prefix="/entity", tags=["Entity"])


# CRUD operations

@router.post("/", response_model=EntityResponse)
async def create_entity(entity_data: EntityCreate, db: Session = Depends(get_db)):
    
    Create a new entity.
    
    new_entity = Entity(name=entity_data.name)
    db.add(new_entity)
    db.commit()
    db.refresh(new_entity)
    return EntityResponse(id=new_entity.id, name=new_entity.name)


@router.get("/", response_model=EntityListResponse)
async def read_entities(db: Session = Depends(get_db)):
    
    Read all entities.
    
    entities = db.query(Entity).all()
    return EntityListResponse(entities=[EntityResponse(id=e.id, name=e.name) for e in entities])


@router.get("/{id}", response_model=EntityResponse)
async def read_entity(id: int, db: Session = Depends(get_db)):
    
    Read a single entity by ID.
    
    entity = db.query(Entity).filter(Entity.id == id).first()
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")
    return EntityResponse(id=entity.id, name=entity.name)


@router.put("/{id}", response_model=EntityResponse)
async def update_entity(id: int, entity_data: EntityUpdate, db: Session = Depends(get_db)):
    
    Update an existing entity.
    
    entity = db.query(Entity).filter(Entity.id == id).first()
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")

    if entity_data.name is not None:
        entity.name = entity_data.name

    db.commit()
    db.refresh(entity)
    return EntityResponse(id=entity.id, name=entity.name)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entity(id: int, db: Session = Depends(get_db)):
    
    Delete an entity by ID.
    
    entity = db.query(Entity).filter(Entity.id == id).first()
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")
    db.delete(entity)
    db.commit()


# Landmark CRUD operations

@router.post("/landmark/", response_model=LandmarkResponse)
async def create_landmark(landmark_data: LandmarkCreate, db: Session = Depends(get_db)):
    
    Create a new landmark.
    
    # Check if the entity exists
    entity = db.query(Entity).filter(Entity.id == landmark_data.entity_id).first()
    if entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")

    new_landmark = Landmark(
        name=landmark_data.name,
        description=landmark_data.description,
        latitude=landmark_data.latitude,
        longitude=landmark_data.longitude,
        entity_id=landmark_data.entity_id,
    )
    db.add(new_landmark)
    db.commit()
    db.refresh(new_landmark)
    return LandmarkResponse(
        id=new_landmark.id,
        name=new_landmark.name,
        description=new_landmark.description,
        latitude=new_landmark.latitude,
        longitude=new_landmark.longitude,
        entity_id=new_landmark.entity_id,
    )


@router.get("/landmark/", response_model=LandmarkListResponse)
async def read_landmarks(db: Session = Depends(get_db)):
    
    Read all landmarks.
    
    landmarks = db.query(Landmark).all()
    return LandmarkListResponse(
        landmarks=[
            LandmarkResponse(
                id=l.id,
                name=l.name,
                description=l.description,
                latitude=l.latitude,
                longitude=l.longitude,
                entity_id=l.entity_id,
            )
            for l in landmarks
        ]
    )


@router.get("/landmark/{id}", response_model=LandmarkResponse)
async def read_landmark(id: int, db: Session = Depends(get_db)):
    
    Read a single landmark by ID.
    
    landmark = db.query(Landmark).filter(Landmark.id == id).first()
    if landmark is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Landmark not found")
    return LandmarkResponse(
        id=landmark.id,
        name=landmark.name,
        description=landmark.description,
        latitude=landmark.latitude,
        longitude=landmark.longitude,
        entity_id=landmark.entity_id,
    )


@router.put("/landmark/{id}", response_model=LandmarkResponse)
async def update_landmark(id: int, landmark_data: LandmarkUpdate, db: Session = Depends(get_db)):
    
    Update an existing landmark.
    
    landmark = db.query(Landmark).filter(Landmark.id == id).first()
    if landmark is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Landmark not found")

    if landmark_data.name is not None:
        landmark.name = landmark_data.name
    if landmark_data.description is not None:
        landmark.description = landmark_data.description
    if landmark_data.latitude is not None:
        landmark.latitude = landmark_data.latitude
    if landmark_data.longitude is not None:
        landmark.longitude = landmark_data.longitude
    if landmark_data.entity_id is not None:
        # Check if the entity exists
        entity = db.query(Entity).filter(Entity.id == landmark_data.entity_id).first()
        if entity is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")
        landmark.entity_id = landmark_data.entity_id

    db.commit()
    db.refresh(landmark)
    return LandmarkResponse(
        id=landmark.id,
        name=landmark.name,
        description=landmark.description,
        latitude=landmark.latitude,
        longitude=landmark.longitude,
        entity_id=landmark.entity_id,
    )


@router.delete("/landmark/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_landmark(id: int, db: Session = Depends(get_db)):
    
    Delete a landmark by ID.
    
    landmark = db.query(Landmark).filter(Landmark.id == id).first()
    if landmark is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Landmark not found")
    db.delete(landmark)
    db.commit()