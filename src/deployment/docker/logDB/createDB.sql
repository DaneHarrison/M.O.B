create table "Entry"
(
    "entryID"    serial,
    "entryPhoto" bytea not null,
    primary key ("entryID")
);

alter table "Entry"
    owner to "user";