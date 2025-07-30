--  Creates tables

CREATE TABLE office (
    name TEXT PRIMARY KEY,
    city TEXT,
    area NUMBER
);

CREATE TABLE agency (
    agency_id INTEGER PRIMARY KEY,
    name TEXT,
    address TEXT,
    city TEXT,
    phone TEXT
);

CREATE TABLE rental (
    rental_id INTEGER PRIMARY KEY,
    office_name TEXT,
    amount REAL,
    end_date INTEGER
);
