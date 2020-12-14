create table users(
    id SERIAL PRIMARY KEY UNIQUE NOT NULL,
    username VARCHAR UNIQUE  NOT NULL,
    password bytea,

    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR UNIQUE,
    phone VARCHAR UNIQUE,
    status VARCHAR
);

create table wallets(
    id SERIAL PRIMARY KEY,
    owner_id INTEGER,

    name VARCHAR,
    balance INTEGER,
    currency VARCHAR,

    FOREIGN KEY (owner_id) REFERENCES users (id)
);
