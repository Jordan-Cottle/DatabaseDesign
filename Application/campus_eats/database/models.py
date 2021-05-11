from database import Base


class Rating(Base):
    """ Reflected class for the rating table. """

    __tablename__ = "rating"

    def __str__(self):
        return f"{self.rating_type.capitalize()} rating for order {self.order_id}: {self.rating_comment}"


class DriverRating(Rating):
    """ Reflected class for the driver_rating table. """

    __tablename__ = "driver_rating"

    def table_str(self):
        """ Generate a string to place in the table when viewed as part of the customer order report. """
        if self.rating_comment:
            return self.rating_comment[:30] + (
                "..." if len(self.rating_comment) > 30 else ""
            )
        else:
            items = []
            if self.driver_speed_rating:
                items.append(f"Speed: {self.driver_speed_rating}")
            if self.driver_friendliness_rating:
                items.append(f"Friendliness: {self.driver_friendliness_rating}")

            return ", ".join(items)

    def __str__(self):
        return f"{super().__str__()} Speed: {self.driver_speed_rating}, Friendliness: {self.driver_friendliness_rating}"


class RestaurantRating(Rating):
    """ Reflected class for the driver_rating table. """

    __tablename__ = "restaurant_rating"

    def table_str(self):
        """ Generate a string to place in the table when viewed as part of the customer order report. """
        if self.rating_comment:
            return self.rating_comment[:30] + (
                "..." if len(self.rating_comment) > 30 else ""
            )
        else:
            items = []
            if self.restaurant_value_rating:
                items.append(f"Value: {self.restaurant_value_rating}")
            if self.restaurant_quality_rating:
                items.append(f"Quality: {self.restaurant_quality_rating}")

            return ", ".join(items)

    def __str__(self):
        return f"{super().__str__()} Value: {self.restaurant_value_rating}, Quality: {self.restaurant_quality_rating}"


class Order(Base):
    """ Reflected class for the order table. """

    __tablename__ = "order"

    def __str__(self) -> str:
        return f"Order {self.order_id} for {self.person.person_name} from {self.restaurant.restaurant_name}"

    __repr__ = __str__
