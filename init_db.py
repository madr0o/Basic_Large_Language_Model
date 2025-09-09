from db import engine, Base
from models import Animal

if __name__ == "__main__":
    Base.metadata.create_all(engine)