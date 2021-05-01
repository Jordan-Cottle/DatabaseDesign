import random

from flask import Flask, g, redirect, render_template, request, url_for
from sqlalchemy.exc import SQLAlchemyError

from database import (
    DriverRating,
    Order,
    RestaurantRating,
    Session,
    add_driver_rating,
    add_restaurant_rating,
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
def order_list():
    # pick random user to "login" if no query param specifies one
    customer_id = request.args.get("customer_id") or get_random_user()

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


@app.route("/orders/<order_id>")
def order_detail(order_id):
    order = g.session.query(Order).filter_by(order_id=order_id).one()

    driver_rating = None
    restaurant_rating = None
    for rating in order.rating_collection:
        if rating.rating_type == "driver":
            assert (
                driver_rating is None
            ), "Whoops, an order should have at most one rating for the driver"

            driver_rating = (
                g.session.query(DriverRating)
                .filter_by(rating_id=rating.rating_id)
                .one()
            )
        else:
            assert (
                restaurant_rating is None
            ), "Whoops, an order should have at most one rating for the restaurant"

            restaurant_rating = (
                g.session.query(RestaurantRating)
                .filter_by(rating_id=rating.rating_id)
                .one()
            )

    return render_template(
        "order.html",
        order=order,
        driver_rating=driver_rating,
        restaurant_rating=restaurant_rating,
    )


@app.route("/orders/<order_id>/rate/driver", methods=["POST"])
def rate_driver(order_id):
    order = g.session.query(Order).filter_by(order_id=order_id).one()

    speed_rating = request.form.get("speed")
    friendliness_rating = request.form.get("friendliness")
    comment = request.form.get("comment") or None

    add_driver_rating(order_id, speed_rating, friendliness_rating, comment)

    return redirect(url_for("order_list", customer_id=order.person_id))


@app.route("/orders/<order_id>/rate/restaurant", methods=["POST"])
def rate_restaurant(order_id):
    order = g.session.query(Order).filter_by(order_id=order_id).one()

    value_rating = request.form.get("value")
    quality_rating = request.form.get("quality")
    comment = request.form.get("comment") or None

    add_restaurant_rating(order_id, value_rating, quality_rating, comment)

    return redirect(url_for("order_list", customer_id=order.person_id))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3000")
