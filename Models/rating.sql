CREATE TABLE `rating` (
  `rating_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `rating_comment` varchar(300) DEFAULT NULL,
  `rating_type` varchar(10) NOT NULL,
  PRIMARY KEY (`rating_id`),
  KEY `rating_order_fk_idx` (`order_id`),
  CONSTRAINT `rating_order_fk` FOREIGN KEY (`order_id`) REFERENCES `order` (`order_id`),
  CONSTRAINT `valid_rating_type_check` CHECK ((`rating_type` in (_utf8mb4'driver',_utf8mb4'restaraunt')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Stores values and comments for all ratings, plus which type of rating it is.';
