# Ratings Business rules
- Customers can (optional) leave a rating for the driver or restaurant associated with their order.
    - Customers cannot rate a restaurant they have not placed an order with
    - Customers cannot rate a driver that has not delivered an order to them

- Ratings are tracked per-order
    - An order can have both a rating for the driver and the restaurant, either, or neither.
    - Customers who order from a restaurant multiple times can leave multiple different ratings for that restaurant

- All ratings are between 1 and 5 stars inclusive

- Customers can view the average and individual ratings for a restaurant at any time.

- Customers cannot see rating data for drivers

- Administrators can view average and individual ratings for a restaurant

- Administrators can view the average and individual ratings for a driver
