from load.database import engine
from load.models import Base

Base.metadata.create_all(engine)

print("Database initialized.")