DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_driver_rating`(
    in _order_id int,
    in _speed_rating tinyint,
    in _friendliness_rating tinyint,
    in _rating_comment varchar(300),
    out _rating_id int
)
BEGIN
    set _rating_id = (
        select rating_id
        from rating
        where
            rating.order_id = _order_id
            and rating_type = 'driver'
    );

    if _rating_id is null then
        insert into `rating`
            (order_id, rating_comment, rating_type)
        values
            (_order_id, _rating_comment, 'driver');

        set _rating_id = (
            select rating_id
            from rating
            where
                rating.order_id = _order_id
                and rating_type = 'driver'
        );

        insert into `driver_rating`
            (rating_id, driver_speed_rating, driver_friendliness_rating)
        values
            (_rating_id, _speed_rating, _friendliness_rating);
    else
        update rating
        set rating_comment = _rating_comment
        where
            rating_id = _rating_id;

        update driver_rating
        set
            driver_speed_rating = _speed_rating,
            driver_friendliness_rating = _friendliness_rating
        where rating_id = _rating_id;
    end if;
END$$
DELIMITER ;
