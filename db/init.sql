create table id (
  id integer PRIMARY KEY, 
  name varchar(10)
);

create table task (
  id serial PRIMARY KEY, 
  user_id integer REFERENCES id(id), 
  title TEXT,
  description TEXT
);

INSERT INTO id(id, name) VALUES(01967, 'sci01967');