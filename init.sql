--
-- Table user
--
DROP TABLE IF EXISTS "user";
DROP TYPE IF EXISTS "role";
CREATE TYPE "role" AS ENUM ('USER', 'ADMIN');

CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(162) NOT NULL,
    role "role" NOT NULL
);

INSERT INTO "user" (email, password, role)
VALUES
    ('validuser@example.com', 'scrypt:32768:8:1$UWtu772MZYNAm2jX$91abb9cb9a9355e445b2c03f183c8c468d8683582fbf4780f7d925be36898052ad5deee83c081081d738c6f15ead5d1ea351367154c5fa6b2a27cfdfe46c6c83', 'USER'),
    ('admin@example.com', 'scrypt:32768:8:1$UWtu772MZYNAm2jX$91abb9cb9a9355e445b2c03f183c8c468d8683582fbf4780f7d925be36898052ad5deee83c081081d738c6f15ead5d1ea351367154c5fa6b2a27cfdfe46c6c83', 'ADMIN');

--
-- Table book
--
DROP TABLE IF EXISTS "book";
DROP TYPE IF EXISTS "language";

CREATE TYPE "language" AS ENUM ('UKR', 'ENG', 'GER');

CREATE TABLE "book" (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    lang "language" NOT NULL,
    age INTEGER NOT NULL,
    pages INTEGER NOT NULL,
    description VARCHAR(500) NOT NULL,
    cover VARCHAR(200) NOT NULL
);

INSERT INTO "book" (title, lang, age, pages, description, cover)
VALUES
    ('Example Book 1', 'ENG', 10, 300, 'This is an example book description.', '/path/to/cover1.jpg'),
    ('Example Book 2', 'UKR', 5, 150, 'This is another example book description.', '/path/to/cover2.jpg'),
    ('Example Book 3', 'GER', 15, 100, 'This is another example book description.', '/path/to/cover3.jpg'),
    ('Example Book 4', 'ENG', 12, 120, 'This is another example book description.', '/path/to/cover4.jpg'),
    ('Example Book 5', 'UKR', 25, 150, 'This is another example book description.', '/path/to/cover5.jpg'),
    ('Example Book 6', 'GER', 35, 90, 'This is another example book description.', '/path/to/cover6.jpg');

--
-- Table user_books
--
DROP TABLE IF EXISTS "user_book";

CREATE TABLE "user_book" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id),
    book_id INTEGER NOT NULL REFERENCES "book"(id),
    start_date DATE,
    end_date DATE
);

INSERT INTO "user_book" (user_id, book_id, start_date, end_date) VALUES
    (1, 1, '2023-01-01', '2023-02-01'),
    (2, 2, '2023-03-01', '2023-04-01'),
    (1, 3, NULL, NULL),
    (1, 4, NULL, '2023-04-01'),
    (1, 5, NULL, NULL),
    (1, 6, '2023-03-01', NULL);

