import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base , get_db
TEST_DATABASE_URL="sqlite:///./test_kuppam.db"
test_engine=create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread":False}
)
TestSeesionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)
def override_get_db():
    db=TestSeesionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db]=override_get_db
@pytest.fixture()
def client():
    Base.metadata.create_all(bind=test_engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=test_engine)