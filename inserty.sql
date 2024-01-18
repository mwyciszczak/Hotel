INSERT INTO city (name) VALUES
    ('Wrocław'),
    ('Kraków'),
    ('Warszawa');

INSERT INTO hotel (name, city_id) VALUES
    ('Hotel Wrocławski', 1),
    ('Hotel Krakowski', 2),
    ('Hotel Warszawski', 3);

INSERT INTO room (number, capacity, hotel_id) VALUES
    (101, 2, 1), (102, 3, 1), (103, 5, 1),
    (201, 2, 2), (202, 3, 2), (203, 5, 2),
    (301, 2, 3), (302, 3, 3), (303, 5, 3);

INSERT INTO restaurant (name, hotel_id) VALUES
    ('Restauracja Wrocławska', 1),
    ('Restauracja Krakowska', 2),
    ('Restauracja Warszawska', 3);

INSERT INTO tables (number, capacity, restaurant_id) VALUES
    (1, 4, 1), (2, 4, 1), (3, 8, 1), (4, 8, 1),
    (1, 4, 2), (2, 4, 2), (3, 8, 2), (4, 8, 2),
    (1, 4, 3), (2, 4, 3), (3, 8, 3), (4, 8, 3);