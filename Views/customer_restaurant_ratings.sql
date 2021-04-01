create view customer_restaurant_ratings as
select
	person_id as customer_id,
    person_name as customer_name,
    restaurant_id,
    restaurant_name,
    rating_value,
    order_id,
    delivery_time
from restaurant_rating
join `order`
	using(order_id)
join person
	using(person_id)
join restaurant
	using(restaurant_id)
join delivery
	using(delivery_id)
order by restaurant_id, delivery_time;