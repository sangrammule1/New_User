from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    name1: str
    email: Optional[str] = None
    is_active: bool = True
    route: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


def test_user_schema():
    user_data = {"id": 1, "name": "John Doe", "name1": "John", "route": "/users/1"}
    user = User(**user_data)
    assert user.id == 1
    assert user.name == "John Doe"
    assert user.name1 == "John"
    assert user.email is None
    assert user.is_active is True
    assert user.route == "/users/1"

    user_data_full = {
        "id": 2,
        "name": "Jane Doe",
        "name1": "Jane",
        "email": "jane.doe@example.com",
        "is_active": False,
        "route": "/users/2",
    }
    user_full = User(**user_data_full)
    assert user_full.id == 2
    assert user_full.name == "Jane Doe"
    assert user_full.name1 == "Jane"
    assert user_full.email == "jane.doe@example.com"
    assert user_full.is_active is False
    assert user_full.route == "/users/2"


def test_item_schema():
    item_data = {"name": "Foo", "price": 50.0}
    item = Item(**item_data)
    assert item.name == "Foo"
    assert item.price == 50.0
    assert item.description is None
    assert item.tax is None

    item_data_full = {
        "name": "Bar",
        "description": "A very nice item",
        "price": 100.0,
        "tax": 10.0,
    }
    item_full = Item(**item_data_full)
    assert item_full.name == "Bar"
    assert item_full.description == "A very nice item"
    assert item_full.price == 100.0
    assert item_full.tax == 10.0