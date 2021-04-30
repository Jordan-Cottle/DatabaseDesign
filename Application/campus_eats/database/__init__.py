from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

Base = automap_base()

from .database import ENGINE
from .models import *
Base.prepare(ENGINE, reflect=True)

Session = sessionmaker(bind=ENGINE)
