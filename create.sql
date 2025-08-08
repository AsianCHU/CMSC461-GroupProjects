CREATE TABLE office (
    office_name TEXT PRIMARY KEY,
    city TEXT,
    area NUMBER
);

CREATE TABLE agency (
    agency_id INTEGER PRIMARY KEY,
    agency_name TEXT,
    address TEXT,
    city TEXT,
    phone TEXT
);

CREATE TABLE rental (
    rental_id INTEGER PRIMARY KEY,
    office_name TEXT,
    amount REAL,
    end_date DATE,
    FOREIGN KEY (office_name) REFERENCES office(office_name)
);

CREATE TABLE agency_and_rental (
    agency_id INTEGER,
    rental_id INTEGER,
    PRIMARY KEY(agency_id, rental_id),
    FOREIGN KEY (agency_id) REFERENCES agency(agency_id),
    FOREIGN KEY (rental_id) REFERENCES rental(rental_id)
);
