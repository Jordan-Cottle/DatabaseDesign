from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

Base = automap_base()

from .database import ENGINE
from .models import *

from .procedures import add_driver_rating, add_restaurant_rating

Base.prepare(ENGINE, reflect=True)

Session = sessionmaker(bind=ENGINE)
