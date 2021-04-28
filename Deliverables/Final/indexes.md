# Query performance
Since the the tables involved in the ratings system hold very little information and rely on foreign keys that are indexed by default the [driver_info](../../Views/driver_info.sql)| [driver_reviews]| [restaurant_reviews]| [driver_ratings]| and [restaurant_ratings] view queries generated very efficient execution plans without needing any additional indexes.

However, queries that filter on the values of the ratings themselves seem to require a lot more processing than necessary without indexes as seen in the following `explain` output.

```sql
explain
select *
from driver_reviews
where friendliness > 3;
```

|id|select_type|table|partitions|type|possible_keys|key|key_len|ref|rows|filtered|Extra|
|--|-----------|-----|----------|----|-------------|---|-------|---|----|--------|-----|
|1|SIMPLE|driver|NULL|index|PRIMARY,fk_D_student_id|fk_D_student_id|4|NULL|8|100.00|"Using index"|
|1|SIMPLE|student|NULL|eq_ref|PRIMARY,fk_St_person_id|PRIMARY|4|campus_eats_fall2020.driver.student_id|1|100.00|NULL|
|1|SIMPLE|person|NULL|eq_ref|PRIMARY|PRIMARY|4|campus_eats_fall2020.student.person_id|1|100.00|NULL|
|1|SIMPLE|driver_rating|NULL|ALL|PRIMARY,driver_rating_subtype_fk_idx|NULL|NULL|NULL|106|33.33|"Using where; Using join buffer (hash join)"|
|1|SIMPLE|rating|NULL|eq_ref|PRIMARY,rating_order_fk_idx|PRIMARY|4|campus_eats_fall2020.driver_rating.rating_id|1|100.00|NULL|
|1|SIMPLE|order|NULL|eq_ref|PRIMARY,fk_O_person_id,fk_O_delivery_id,fk_O_driver_id|PRIMARY|4|campus_eats_fall2020.rating.order_id|1|12.50|"Using where"|
|1|SIMPLE|customer|NULL|eq_ref|PRIMARY|PRIMARY|4|campus_eats_fall2020.order.person_id|1|100.00|NULL|
|1|SIMPLE|delivery|NULL|eq_ref|PRIMARY|PRIMARY|4|campus_eats_fall2020.order.delivery_id|1|100.00|NULL|


Even though the query only returns 27 rows given the test data, it has to look through the full 106 rows that were in the table when the query was ran.

Using an index should hopefully allow the database to more easily identify the needed rows so that fewer unneeded rows can be accessed.

# Adding indexes

Since filtering by value of the results seems like a common task that an administrator or user would like to do to answer questions like "What do the positive reviews for a restaurant say?" or "What do the negative reviews for the new drivers on the team say?" the different ratings criteria for the ratings tables will often appear in where clauses. To speed up query processing indexes should be created for each of the two ratings value columns in each of the two ratings sub-type tables.

The sql for adding them is as follows:
```sql
CREATE INDEX driver_friendliness_rating_idx ON driver_rating (driver_friendliness_rating);
CREATE INDEX driver_speed_rating_idx ON driver_rating (driver_speed_rating);
CREATE INDEX restaurant_value_rating_idx ON restaurant_rating (restaurant_value_rating);
CREATE INDEX restaurant_quality_rating_idx ON restaurant_rating (restaurant_quality_rating);
```

After adding them, the explain output for the query mentioned above shows a much more efficient query.

|id|select_type|table|partitions|type|possible_keys|key|key_len|ref|rows|filtered|Extra|
|--|-----------|-----|----------|----|-------------|---|-------|---|----|--------|-----|
|1|SIMPLE|driver_rating|NULL|range|PRIMARY,driver_rating_subtype_fk_idx,driver_friendliness_rating_idx|driver_friendliness_rating_idx|2|NULL|27|100.00|"Using index condition"|
|1|SIMPLE|rating|NULL|eq_ref|PRIMARY,rating_order_fk_idx|PRIMARY|4|campus_eats_fall2020.driver_rating.rating_id|1|100.00|NULL|
|1|SIMPLE|order|NULL|eq_ref|PRIMARY,fk_O_person_id,fk_O_delivery_id,fk_O_driver_id|PRIMARY|4|campus_eats_fall2020.rating.order_id|1|100.00|NULL|
|1|SIMPLE|delivery|NULL|eq_ref|PRIMARY|PRIMARY|4|campus_eats_fall2020.order.delivery_id|1|100.00|NULL|
|1|SIMPLE|driver|NULL|eq_ref|PRIMARY,fk_D_student_id|PRIMARY|4|campus_eats_fall2020.order.driver_id|1|100.00|NULL|
|1|SIMPLE|student|NULL|eq_ref|PRIMARY,fk_St_person_id|PRIMARY|4|campus_eats_fall2020.driver.student_id|1|100.00|NULL|
|1|SIMPLE|person|NULL|eq_ref|PRIMARY|PRIMARY|4|campus_eats_fall2020.student.person_id|1|100.00|NULL|
|1|SIMPLE|customer|NULL|eq_ref|PRIMARY|PRIMARY|4|campus_eats_fall2020.order.person_id|1|100.00|NULL|

The query optimizer is able to make use of an index or const comparison for every step in the query and only has to look at the 27 rows that get returned in the result where before it required a full table scan of the desired ratings subtype table.

# Reverse queries

Even after the index is added, not all queries seem to make use of it. The following query is very similar to the first one that uses the index perfectly, but fails to generate an explain plan that makes use of the index.

```sql
explain
select *
from driver_reviews
where friendliness > 3;
```

|id|select_type|table|partitions|type|possible_keys|key|key_len|ref|rows|filtered|Extra|
|--|-----------|-----|----------|----|-------------|---|-------|---|----|--------|-----|
|1|SIMPLE|driver|NULL|index|PRIMARY,fk_D_student_id|fk_D_student_id|4|NULL|8|100.00|"Using index"|
|1|SIMPLE|student|NULL|eq_ref|PRIMARY,fk_St_person_id|PRIMARY|4|campus_eats_fall2020.driver.student_id|1|100.00|NULL|
|1|SIMPLE|person|NULL|eq_ref|PRIMARY|PRIMARY|4|campus_eats_fall2020.student.person_id|1|100.00|NULL|
|1|SIMPLE|driver_rating|NULL|ALL|PRIMARY,driver_rating_subtype_fk_idx,driver_friendliness_rating_idx,driver_friendliness_rating_desc_idx|NULL|NULL|NULL|106|41.51|"Using where; Using join buffer (hash join)"|
|1|SIMPLE|rating|NULL|eq_ref|PRIMARY,rating_order_fk_idx|PRIMARY|4|campus_eats_fall2020.driver_rating.rating_id|1|100.00|NULL|
|1|SIMPLE|order|NULL|eq_ref|PRIMARY,fk_O_person_id,fk_O_delivery_id,fk_O_driver_id|PRIMARY|4|campus_eats_fall2020.rating.order_id|1|12.50|"Using where"|
|1|SIMPLE|customer|NULL|eq_ref|PRIMARY|PRIMARY|4|campus_eats_fall2020.order.person_id|1|100.00|NULL|
|1|SIMPLE|delivery|NULL|eq_ref|PRIMARY|PRIMARY|4|campus_eats_fall2020.order.delivery_id|1|100.00|NULL|

Searching through documentation I found that MySql supports a [descending index](https://dev.mysql.com/doc/refman/8.0/en/descending-indexes.html).

However, after adding a descending index to the `driver_rating` table the explain plan remained the same.

```sql
CREATE INDEX driver_friendliness_rating_desc_idx ON driver_rating (driver_friendliness_rating desc);
```

I thought perhaps the complex query through the view was somehow confusing the optimizer, but a direct query against the `driver_rating` table produced an explain plan with a full table scan as well.

```sql
explain
select *
from driver_rating
where driver_friendliness_rating < 3;
```

|id|select_type|table|partitions|type|possible_keys|key|key_len|ref|rows|filtered|Extra|
|--|-----------|-----|----------|----|-------------|---|-------|---|----|--------|-----|
|1|SIMPLE|driver_rating|NULL|ALL|driver_friendliness_rating_idx,driver_friendliness_rating_desc_idx|NULL|NULL|NULL|106|41.51|"Using where"|

Even with an index in both directions it seems the optimizer thinks a full table scan is more efficient than using the descending index.

The behavior was still observed even after running `analyze table driver_rating;` to ensure the optimizer had the most up-to-date information to make decisions with.

It would be interesting to generate a much larger volume of test data to see if the optimizer would make a different decision if it knew there were far more unnecessary rows to process.
