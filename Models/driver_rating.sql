CREATE TABLE `driver_rating` (
  `driver_rating_id` int PRIMARY KEY AUTO_INCREMENT,
  `rating_value` tinyint unsigned NOT NULL,
  `order_id` int NOT NULL,
  UNIQUE KEY `order_id_UNIQUE` (`order_id`),
  KEY `order_fk_idx` (`order_id`),
  CONSTRAINT `driver_rating_order_fk` FOREIGN KEY (`order_id`) REFERENCES `order` (`order_id`),
  CONSTRAINT `valid_driver_rating_check` CHECK ((`rating_value` >= 1) and (`rating_value` <= 5))
) COMMENT='Tracks individual ratings for restaurants';