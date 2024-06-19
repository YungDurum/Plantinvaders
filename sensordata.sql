CREATE TABLE plants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE saturation_data (
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
    id INTEGER, 
    saturation DECIMAL(5,4) CHECK (saturation >= 0 AND saturation <= 1),
    FOREIGN KEY(id) REFERENCES plants(id)
);
CREATE TABLE phonenumbers (
    name TEXT NOT NULL,
    phone TEXT NOT NULL
);




