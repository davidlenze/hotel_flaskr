drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    date text ,
    room text not null,
    customer text,
    recordno integer
);
