-- noinspection SqlWithoutWhereForFile

-- Clear values

DELETE
FROM core_repayment;
DELETE
FROM core_deposit;
DELETE
FROM core_member;
DELETE
FROM core_event;
DELETE
FROM authtoken_token;
DELETE
FROM auth_user;
DELETE
FROM core_profile;
DELETE
FROM auth_user;

-- Insert testdata
-- Common password: pwForEvery1

INSERT INTO auth_user (id, password, is_superuser, username, last_name, email, is_staff, is_active,
                       date_joined, first_name)
VALUES (1, 'pbkdf2_sha256$600000$UUl8gfz7rSdoLuHvfQRn97$fkJ/kytR67cemFmEo919mIw+o6tf9+G03qiAT9dNLW8=', 0,
        'falser', 'Krupenkov', 'kno3.2002@gmail.com', 0, 1, '2023-10-07 07:10:25.176271', 'Mikhail'),
       (2, 'pbkdf2_sha256$600000$Xo936JQsWO9QNd1Lfn9270$C44ZcgEvoV7OBQrb+iV12rBD1IrK0DuG47YGQAKhNXM=', 0, 'user2',
        '2', 'user2@gmail.com', 0, 1, '2023-10-07 07:11:10.997301', 'User'),
       (3, 'pbkdf2_sha256$600000$rimE4rGhwSfGIKdcTQNT5z$lssHajbR9+RuclfgEoT7PgRGWG3RLwOgA7qleF/wqTk=', 0, 'user3',
        '3', 'user3@gmail.com', 0, 1, '2023-10-07 07:11:10.997301', 'User'),
       (4, 'pbkdf2_sha256$600000$hk1ifYCSnof8OXb6FLeULC$qPL7xct+whpp4depgm/jTkHQSfedK2B1S7JEyV25Jko=', 0, 'user4',
        '4', 'user4@gmail.com', 0, 1, '2023-10-07 07:11:10.997301', 'User');

INSERT INTO core_profile (auth_user_id)
VALUES (1),
       (2),
       (3),
       (4);

INSERT INTO authtoken_token (key, created, user_id)
VALUES ('falser57f95c7f08f1bab7ade43a1c985678b9ce', '2023-10-07 07:10:25.806281', 1),
       ('user2fb3398d4ff870cf4531d3065d034c0c5834', '2023-10-07 07:11:11.620145', 2),
       ('user3be7f95c7f08f1bab7ade43a1c985678b9ce', '2023-10-07 07:11:11.620145', 3),
       ('user4c8224b8e4551782dcfaa693b9e540a5cba0', '2023-10-07 07:11:11.620145', 4);

INSERT INTO core_event (id, date, description, is_closed)
VALUES (1, '2023-10-07', 'Event falser and user2', 0),
       (2, '2023-10-08', 'Event everyone', 0),
       (3, '2023-10-09', 'Event users 2, 3, 4', 0),
       (4, '2023-10-10', 'Event user only falser', 0),
       (5, '2023-10-11', 'Event closed falser and user3', 1);

INSERT INTO core_member (id, event_id, user_id)
VALUES (1, 1, 1),
       (2, 1, 2),
       (3, 2, 1),
       (4, 2, 2),
       (5, 2, 3),
       (6, 2, 4),
       (7, 3, 2),
       (8, 3, 3),
       (9, 3, 4),
       (10, 4, 1),
       (11, 5, 1),
       (12, 5, 3);

INSERT INTO core_deposit (member_id, value, description)
VALUES (1, 10, 'Beer'),
       (2, 5, 'Chips'),
       (4, 14.23, 'Package 1'),
       (5, 30.60, 'Package 2'),
       (9, 20, 'Food'),
       (11, 5, 'Tickets'),
       (12, 15, 'Popcorn');

INSERT INTO core_repayment (event_id, payer_id, recipient_id, value)
VALUES (2, 3, 5, 10),
       (5, 12, 11, 10);
