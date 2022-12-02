create table "Entry"
(
    "entryID"    serial,
    "entryPhoto" bytea not null,
    primary key ("entryID")
);

alter table "Entry"
    owner to "user";

create unique index "Entry_entryPhoto_key"
    on "Entry" ("entryPhoto");

