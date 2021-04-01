create view customer_driver_ratings as
select
	p1.person_id as customer_id,
    p1.person_name as customer_name,
    driver.driver_id,
    p2.person_name as driver_name,
    rating_value,
    order_id,
    delivery_time
from driver_rating
join `order`
	using(order_id)
join person as p1
	using(person_id)
join driver
	using(driver_id)
join student
	using(student_id)
join person as p2
	on student.person_id = p2.person_id
join delivery
	using(delivery_id)
order by driver.driver_id, delivery_time;