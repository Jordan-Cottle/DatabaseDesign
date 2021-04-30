from sqlalchemy.orm import sessionmaker

from .database import ENGINE
Session = sessionmaker(bind=ENGINE)
