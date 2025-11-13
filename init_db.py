from app.core.Database import Base, engine
from app.models.User import User
from app.models.Video import Video
from app.models.Template import Template

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
print("Tables: users, videos, templates")
