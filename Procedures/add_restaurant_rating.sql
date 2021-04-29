DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_restaurant_rating`(
    in _order_id int,
    in _value_rating tinyint,
    in _quality_rating tinyint,
    in _rating_comment varchar(300),
    out _rating_id int
)
BEGIN
    set _rating_id = (
        select rating_id
        from rating
        where
            rating.order_id = _order_id
            and rating_type = 'restaurant'
    );

    if _rating_id is null then
        insert into `rating`
            (order_id, rating_comment, rating_type)
        values
            (_order_id, _rating_comment, 'restaurant');

        set _rating_id = (
            select rating_id
            from rating
            where
                rating.order_id = _order_id
                and rating_type = 'restaurant'
        );

        insert into `restaurant_rating`
            (rating_id, restaurant_value_rating, restaurant_quality_rating)
        values
            (_rating_id, _value_rating, _quality_rating);
    else
        update rating
        set rating_comment = _rating_comment
        where
            rating_id = _rating_id;

        update restaurant_rating
        set
            restaurant_value_rating = _value_rating,
            restaurant_quality_rating = _quality_rating
        where rating_id = _rating_id;
    end if;
END$$
DELIMITER ;
