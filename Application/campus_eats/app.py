import random

from flask import Flask, g, render_template, request
from sqlalchemy.exc import SQLAlchemyError

from database import (
    DriverRating,
    Order,
    RestaurantRating,
    Session,
)

app = Flask(__name__)


@app.before_request
def inject_session():
    g.session = Session()


@app.after_request
def close_session(response):
    try:
        g.session.commit()
    except SQLAlchemyError:
        g.session.rollback()
    finally:
        g.session.close()

    return response


@app.route("/")
def index():
    return render_template("index.html")


AVG_DRIVER_COLS = [
    "driver_id",
    "name",
    "avg_speed_rating",
    "avg_friendliness_rating",
    "num_ratings",
]

AVG_RESTAURANT_COLS = [
    "restaurant_id",
    "name",
    "avg_value_rating",
    "avg_quality_rating",
    "num_ratings",
]


@app.route("/admin")
def admin_view():
    """Query aggregated data from database."""
    driver_data = g.session.execute("select * from avg_driver_ratings").fetchall()
    drivers = [dict(zip(AVG_DRIVER_COLS, driver)) for driver in driver_data]

    restaurant_data = g.session.execute(
        "select * from avg_restaurant_ratings"
    ).fetchall()
    restaurants = [
        dict(zip(AVG_RESTAURANT_COLS, restaurant)) for restaurant in restaurant_data
    ]

    return render_template("admin.html", drivers=drivers, restaurants=restaurants)


def get_random_user():
    """Pick a random user to login."""
    customers_with_orders = g.session.execute(
        "select distinct person_id from `order`"
    ).fetchall()

    return random.choice(customers_with_orders)[0]


@app.route("/orders")
def customer_view():
    # pick random user to "login" as
    customer_id = get_random_user()

    orders = g.session.query(Order).filter_by(person_id=customer_id).all()

    ratings = []
    for order in orders:
        ratings.extend(order.rating_collection)

    driver_ratings = {}
    restaurant_ratings = {}
    for rating in ratings:
        order_id = rating.order_id
        if rating.rating_type == "driver":
            driver_ratings[order_id] = (
                g.session.query(DriverRating)
                .filter_by(rating_id=rating.rating_id)
                .one()
            )
        else:
            restaurant_ratings[order_id] = (
                g.session.query(RestaurantRating)
                .filter_by(rating_id=rating.rating_id)
                .one()
            )

    return render_template(
        "orders.html",
        orders=orders,
        driver_ratings=driver_ratings,
        restaurant_ratings=restaurant_ratings,
    )




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="3000")
