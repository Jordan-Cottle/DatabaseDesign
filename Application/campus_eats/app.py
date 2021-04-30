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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="3000")
