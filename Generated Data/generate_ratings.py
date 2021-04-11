from random import randint, random, choice
from collections import defaultdict
from urllib.request import urlopen

SQL_INSERT_TEMPLATE = """insert into `{table}` ({columns}) values
  {values};"""

with open("orders.csv", 'r') as orders_data:
    orders_data.readline()  # skip header row
    ORDER_IDS = [line.split(",")[0] for line in orders_data]


RATING_COLUMNS = "`rating_id`,`order_id`,`rating_comment`,`rating_type`"
DRIVER_RATING_COLUMNS = "`rating_id`,`driver_speed_rating`,`driver_friendliness_rating`"
RESTAURANT_RATING_COLUMNS = (
    "`rating_id`,`restaurant_value_rating`,`restaurant_quality_rating`"
)

DRIVER_RATING = "driver_rating"
RESTAURANT_RATING = "restaurant_rating"

RATING_TYPES = (DRIVER_RATING, RESTAURANT_RATING)

SUPER_RATINGS = []
DRIVER_RATINGS = []
RESTAURANT_RATINGS = []
RATINGS = defaultdict(lambda: set())


def counter():
    i = 1
    while True:
        yield i
        i += 1


RATING_ID_SEQUENCE = counter()


def generate_sub_rating(rating_id):
    data = [rating_id, "null", "null"]

    for _ in range(2):
        data[randint(1, 2)] = str(randint(1, 5))

    return data




def generate_rating(order_id, sub_type):

    rating_id = str(next(RATING_ID_SEQUENCE))

    if random() < 0.25:  # Only make comment for ~25% of ratings
        with urlopen("https://loripsum.net/api/1/short/plaintext") as lorem_ipsum_text:
            comment = lorem_ipsum_text.read().decode().strip()

        if len(comment) > 300:
            # Comment too long, don't use
            comment = "null"
        else:
            comment = f"'{comment}'"
    else:
        comment = "null"

    assert sub_type not in RATINGS[order_id], "Don't add multiple ratings of same subtype for same order"
    RATINGS[order_id].add(sub_type)

    rating_data = [rating_id, order_id, comment, f"'{sub_type.split('_')[0]}'"]
    SUPER_RATINGS.append(rating_data)

    sub_type_data = generate_sub_rating(rating_id)
    if sub_type == DRIVER_RATING:
        DRIVER_RATINGS.append(sub_type_data)
    else:
        RESTAURANT_RATINGS.append(sub_type_data)

def build_sql(table, columns, ratings):
    values = (f"({','.join(rating)})" for rating in ratings)

    return SQL_INSERT_TEMPLATE.format(table=table, columns=columns, values=",\n  ".join(values))

def main():
    for order_id in ORDER_IDS:
        for _ in range(2):
            if random() < 0.25:
                break

            sub_type = choice(RATING_TYPES)
            if sub_type in RATINGS[order_id]:
                continue

            generate_rating(order_id, sub_type)

    print(build_sql("rating", RATING_COLUMNS, SUPER_RATINGS))
    print()
    print(build_sql("driver_rating", DRIVER_RATING_COLUMNS, DRIVER_RATINGS))
    print()
    print(build_sql("restaurant_rating", RESTAURANT_RATING_COLUMNS, RESTAURANT_RATINGS))
    print()


if __name__ == "__main__":
    main()
