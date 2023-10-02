CREATE TABLE request_history (
    id          SERIAL PRIMARY KEY,
    req_photo   BYTEA NOT NULL,
    req_time    DATE NOT NULL DEFAULT CURRENT_DATE
);