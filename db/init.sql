create table id (
  id TEXT PRIMARY KEY, 
  name varchar(10)
);

create table task (
  id serial PRIMARY KEY, 
  user_id TEXT REFERENCES id(id), 
  title TEXT,
  description TEXT
);

INSERT INTO id(id, name) VALUES('sci01967', 'sci01967');