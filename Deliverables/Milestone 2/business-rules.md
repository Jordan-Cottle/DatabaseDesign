# Ratings Business rules
- Customers can (optional) leave a rating for the driver or restaurant associated with their order.
    - Customers cannot rate a restaurant they have not placed an order with
    - Customers cannot rate a driver that has not delivered an order to them

- Ratings are tracked per-order
    - An order can have both a rating for the driver and the restaurant, either, or neither.
    - Customers who order from a restaurant multiple times can leave multiple different ratings for that restaurant (one per order to that restaurant)
    - Customers who receive the same delivery driver multiple times can leave multiple different ratings for that driver (one per order that was delivered to them by that driver)

- Customers can leave a generic text comment as part of their rating to provide additional context/information

- Restaurant can be rated on two different criteria
  - Value -- Was the price fo the food worth it?
  - Quality -- Was the food good?
 - Drivers can be rated on two different criteria
  - Speed -- Did the driver deliver the food promptly?
  - Friendliness -- Did the driver do anything extra to make the experience pleasant?

- All ratings are between 1 and 5 stars inclusive

- Customers can view the average and individual ratings for a restaurant at any time.
  - When viewing individual ratings, customers can see any comments left as part of each rating

- Customers cannot see rating data for drivers

- Administrators can view average and individual ratings for a restaurant

- Administrators can view the average and individual ratings for a driver
