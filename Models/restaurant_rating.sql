CREATE TABLE `restaurant_rating` (
  `restaurant_rating_id` int PRIMARY KEY AUTO_INCREMENT,
  `rating_value` tinyint unsigned NOT NULL,
  `order_id` int NOT NULL,
  UNIQUE KEY `order_id_UNIQUE` (`order_id`),
  KEY `order_fk_idx` (`order_id`),
  CONSTRAINT `restaurant_rating_order_fk` FOREIGN KEY (`order_id`) REFERENCES `order` (`order_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `valid_restaurant_rating_check` CHECK ((`rating_value` >= 1) and (`rating_value` <= 5))
) COMMENT='Tracks individual ratings for restaurants';