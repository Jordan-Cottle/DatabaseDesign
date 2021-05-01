from enum import Enum
from database import ENGINE


class Procedure(str, Enum):
    """ Enumeration of known stored procedures on the database. """

    ADD_DRIVER_RATING = "add_driver_rating"
    ADD_RESTAURANT_RATING = "add_restaurant_rating"


# Data structure for mapping procedure to expected arguments
PROCEDURE_ARGS = {
    Procedure.ADD_DRIVER_RATING: {
        "in": ["order_id", "speed_rating", "friendliness_rating", "rating_comment"],
        "out": ["rating_id"],
    },
    Procedure.ADD_RESTAURANT_RATING: {
        "in": ["order_id", "value_rating", "quality_rating", "rating_comment"],
        "out": ["rating_id"],
    },
}


def build_procedure_call(procedure):
    """ Build a function that will perform a stored procedure call and return the result. """

    assert isinstance(
        procedure, Procedure
    ), "Use the Procedure enum to specify which stored procedure to run"

    def procedure_call(*args):

        procedure_args = PROCEDURE_ARGS[procedure]
        assert len(args) == len(
            procedure_args["in"]
        ), f"{procedure} call expected {len(procedure_args['in'])} arguments but received {len(args)} instead"

        connection = ENGINE.raw_connection()
        try:
            cursor = connection.cursor()
            results = cursor.callproc(procedure, [*args, *procedure_args["out"]])

            # If there was only one out param, return it directly
            if len(procedure_args["out"]) == 1:
                results = results[-1]
            else:
                results = results[len(args) :]

            cursor.close()
            connection.commit()
        finally:
            connection.close()

        return results

    return procedure_call


add_driver_rating = build_procedure_call(Procedure.ADD_DRIVER_RATING)
add_restaurant_rating = build_procedure_call(Procedure.ADD_RESTAURANT_RATING)
