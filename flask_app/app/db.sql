drop table if exists blog;
create table if not exists blog (
  id      integer primary key autoincrement,
  title   varchar not null,
  content varchar
);