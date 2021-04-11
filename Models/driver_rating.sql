CREATE TABLE `driver_rating` (
  `rating_id` int NOT NULL,
  `driver_speed_rating` tinyint unsigned DEFAULT NULL,
  `driver_friendliness_rating` tinyint unsigned DEFAULT NULL,
  PRIMARY KEY (`rating_id`),
  KEY `driver_rating_subtype_fk_idx` (`rating_id`),
  CONSTRAINT `driver_rating_subtype_fk` FOREIGN KEY (`rating_id`) REFERENCES `rating` (`rating_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `driver_friendliness_rating_range_check` CHECK (((`driver_friendliness_rating` is null) or ((`driver_friendliness_rating` >= 1) and (`driver_friendliness_rating` <= 5)))),
  CONSTRAINT `driver_rating_value_required` CHECK (((`driver_speed_rating` is not null) or (`driver_friendliness_rating` is not null))),
  CONSTRAINT `driver_speed_rating_range_check` CHECK (((`driver_speed_rating` is null) or ((`driver_speed_rating` >= 1) and (`driver_speed_rating` <= 5))))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Track values for driver ratings';
