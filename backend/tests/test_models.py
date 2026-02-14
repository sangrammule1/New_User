from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    route = Column(String)

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def test_add_route_field():
    new_user = User(name="John Doe", email="john.doe@example.com", route="Main Street")
    session.add(new_user)
    session.commit()

    retrieved_user = session.query(User).filter_by(name="John Doe").first()
    assert retrieved_user is not None
    assert retrieved_user.route == "Main Street"

def test_user_creation():
    new_user = User(name="Jane Doe", email="jane.doe@example.com")
    session.add(new_user)
    session.commit()

    retrieved_user = session.query(User).filter_by(name="Jane Doe").first()
    assert retrieved_user is not None
    assert retrieved_user.name == "Jane Doe"
    assert retrieved_user.email == "jane.doe@example.com"
    assert hasattr(retrieved_user, 'route') is False

def test_user_fields():
    new_user = User(name="Test User", email="test@example.com", route="Elm Avenue")
    session.add(new_user)
    session.commit()

    retrieved_user = session.query(User).filter_by(name="Test User").first()
    assert retrieved_user.name == "Test User"
    assert retrieved_user.email == "test@example.com"
    assert retrieved_user.route == "Elm Avenue"
    assert retrieved_user.id is not None