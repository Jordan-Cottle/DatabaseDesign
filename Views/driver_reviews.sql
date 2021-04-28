create or replace view `driver_reviews` as
select
	delivery_time as `date`,
    driver.driver_id,
    driver.name as driver_name,
    order_id,
    customer.person_id as customer_id,
    customer.person_name as customer_name,
    driver_speed_rating as speed,
    driver_friendliness_rating as friendliness,
    rating_comment as comment
from driver_rating
join rating using(rating_id)
join `order` using(order_id)
join driver_info as driver using(driver_id)
join person as customer
	on `order`.person_id = customer.person_id
join delivery using(delivery_id);
