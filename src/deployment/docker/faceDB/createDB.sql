create table "UserFaces"
(
    "userID"     serial,
    "userName"   text  not null,
    "userWeight" double precision[],
    "userPhoto"  bytea not null,
    primary key ("userID")
);

alter table "UserFaces"
    owner to "user";