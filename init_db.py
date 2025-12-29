# init_db.py
from db import Base, engine
import models

Base.metadata.create_all(bind=engine)
print("✅ Database tables created.")