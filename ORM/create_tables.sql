CREATE TABLE users (
    id SERIAL NOT NULL,
    username VARCHAR,
    "firstName" VARCHAR,
    "lastName" VARCHAR,
    email VARCHAR,
    password BYTEA,
    phone VARCHAR,
    "userAuthStatus" userstatus,
    PRIMARY KEY (id)
);

CREATE TABLE wallets (
    id SERIAL NOT NULL,
    name VARCHAR,
    balance INTEGER,
    currency currency,
    user_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);
