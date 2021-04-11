CREATE TABLE `restaurant_rating` (
  `rating_id` int NOT NULL,
  `restaurant_value_rating` tinyint unsigned DEFAULT NULL,
  `restaurant_quality_rating` tinyint unsigned DEFAULT NULL,
  PRIMARY KEY (`rating_id`),
  KEY `restaurant_rating_subtype_fk_idx` (`rating_id`),
  CONSTRAINT `restaurant_rating_subtype_fk` FOREIGN KEY (`rating_id`) REFERENCES `rating` (`rating_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `restaurant_quality_rating_range_check` CHECK (((`restaurant_quality_rating` is null) or ((`restaurant_quality_rating` >= 1) and (`restaurant_quality_rating` <= 5)))),
  CONSTRAINT `restaurant_rating_value_required` CHECK (((`restaurant_value_rating` is not null) or (`restaurant_quality_rating` is not null))),
  CONSTRAINT `restaurant_value_rating_range_check` CHECK (((`restaurant_value_rating` is null) or ((`restaurant_value_rating` >= 1) and (`restaurant_value_rating` <= 5))))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Track values for restaraunt ratings. Restaraunts can be rated on their value (was the food affordable?) and their quality (did it taste good?)';
