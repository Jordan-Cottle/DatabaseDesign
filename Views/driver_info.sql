create or replace view `driver_info` as
select
	driver_id,
    student_id,
    person_id,
    person_name as 'name',
    date_hired,
    graduation_year,
    person_email as email,
    cell
    license_number
from driver
join student using(student_id)
join person using(person_id);
