CREATE table IF NOT EXISTS users (

    id VARCHAR(25) PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    password VARCHAR(255) NOT NULL

);