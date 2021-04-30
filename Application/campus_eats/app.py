from flask import Flask, render_template, g
from sqlalchemy.exc import SQLAlchemyError


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
    "num_ratings"
]

AVG_RESTAURANT_COLS = [
    "restaurant_id",
    "name",
    "avg_value_rating",
    "avg_quality_rating",
    "num_ratings"
]

@app.route("/admin")
def admin_view():
    """ Query aggregated data from database. """
    driver_data = g.session.execute("select * from avg_driver_ratings").fetchall()
    drivers = [
        dict(zip(AVG_DRIVER_COLS, driver)) for driver in driver_data
    ]

    restaurant_data = g.session.execute("select * from avg_restaurant_ratings").fetchall()
    restaurants = [
        dict(zip(AVG_RESTAURANT_COLS, restaurant)) for restaurant in restaurant_data
    ]

    return render_template("admin.html", drivers=drivers, restaurants=restaurants)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="3000")
