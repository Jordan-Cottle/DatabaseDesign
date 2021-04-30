from database import Base

class Rating(Base):
    """ Reflected class for the rating table. """
    __tablename__ = "rating"

    def __str__(self):
        return f"{self.rating_type.capitalize()} rating for order {self.order_id}: {self.rating_comment}"

class DriverRating(Rating):
    """ Reflected class for the driver_rating table. """
    __tablename__ = "driver_rating"

    def __str__(self):
        return f"{super().__str__()} Speed: {self.driver_speed_rating}, Friendliness: {self.driver_friendliness_rating}"

class RestaurantRating(Rating):
    """ Reflected class for the driver_rating table. """
    __tablename__ = "restaurant_rating"

    def __str__(self):
        return f"{super().__str__()} Value: {self.restaurant_value_rating}, Quality: {self.restaurant_quality_rating}"

class Order(Base):
    """ Reflected class for the order table. """

    __tablename__ = "order"

    def __str__(self) -> str:
        return f"Order {self.order_id} for {self.person.person_name} from {self.restaurant.restaurant_name}"

    __repr__ = __str__
