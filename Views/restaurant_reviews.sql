create or replace view `restaraunt_reviews` as
select
	delivery_time as `date`,
    restaurant_id,
    restaurant_name,
    order_id,
    person_id,
    person_name,
    restaurant_value_rating as `value`,
    restaurant_quality_rating as quality,
    rating_comment as comment
from restaurant_rating
join rating using(rating_id)
join `order` using(order_id)
join restaurant using(restaurant_id)
join person using(person_id)
join delivery using(delivery_id);
