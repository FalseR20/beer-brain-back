INSERT INTO auth_user (id, password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name) VALUES (1, 'pbkdf2_sha256$600000$tZKESf9Hl7dypRpN4643mJ$F2p0L1p6oqAwkHhZWsQOOup6iYwFSbJbvQsXKXnkRUA=', null, 0, 'falser', 'Krupenkov', 'kno3.2002@gmail.com', 0, 1, '2023-10-07 07:10:25.176271', 'Mikhail');
INSERT INTO auth_user (id, password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name) VALUES (2, 'pbkdf2_sha256$600000$yVpgD2GyVZa4rYkruqhMH4$9EDSUActAir8urkGyWRCIaCtuupoHPb2IkTphMGwygQ=', null, 0, 'user2', '2', 'user2@gmail.com', 0, 1, '2023-10-07 07:11:10.997301', 'User');

INSERT INTO core_profile (auth_user_id) VALUES (1);
INSERT INTO core_profile (auth_user_id) VALUES (2);

INSERT INTO authtoken_token (key, created, user_id) VALUES ('bd0586e7f95c7f08f1bab7ade43a1c985678b9ce', '2023-10-07 07:10:25.806281', 1);
INSERT INTO authtoken_token (key, created, user_id) VALUES ('694463b3398d4ff870cf4531d3065d034c0c5834', '2023-10-07 07:11:11.620145', 2);

INSERT INTO core_event (id, date, description, is_closed) VALUES (1, '2023-10-07', 'Test event 1', 0);

INSERT INTO core_member (id, event_id, user_id) VALUES (1, 1, 1);
INSERT INTO core_member (id, event_id, user_id) VALUES (2, 1, 2);

INSERT INTO core_deposit (id, value, description, member_id) VALUES (1, 10, 'Beer', 1);

INSERT INTO core_repayment (id, value, event_id, payer_id, recipient_id) VALUES (1, 5, 1, 2, 1);
