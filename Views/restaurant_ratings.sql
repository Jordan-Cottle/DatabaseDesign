create or replace view `avg_restaurant_ratings` as
select
    restaurant_id,
    restaurant_name as name,
    round(avg(restaurant_value_rating), 2) as avg_value_rating,
    round(avg(restaurant_quality_rating), 2) as avg_quality_rating,
    count(distinct `order`.order_id) as num_ratings
from restaurant_rating
join rating using(rating_id)
join `order` using(order_id)
join restaurant using(restaurant_id)
group by restaurant_id, name;
