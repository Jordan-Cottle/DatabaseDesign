create or replace view `avg_driver_ratings` AS
select
    driver_id,
    name,
    round(avg(driver_speed_rating), 2) as avg_speed_rating,
    round(avg(driver_friendliness_rating), 2) as avg_friendliness_rating,
    count(distinct `order`.order_id) as num_ratings
from driver_rating
join rating using(rating_id)
join `order` using(order_id)
join driver_info using(driver_id)
group by driver_id, name;
