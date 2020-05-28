# DROP TABLES

songplay_table_drop = """
DROP TYPE IF EXISTS membership_level;
DROP TABLE IF EXISTS songplays;
"""
user_table_drop = """
DROP TYPE IF EXISTS users_gender;
DROP TABLE IF EXISTS users;"""
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TYPE membership_level AS ENUM ('free', 'paid');

CREATE TABLE IF NOT EXISTS songplays (
    songplay_id int PRIMARY KEY,
    start_time timestamp NOT NULL,
    level membership_level NOT NULL,
    song_id char(18) NOT NULL,
    artist_id char(18) NOT NULL,
    session_id int NOT NULL,
    location varchar NOT NULL,
    user_agent varchar NOT NULL
);
""")

user_table_create = ("""
CREATE TYPE users_gender AS ENUM ('F', 'M');

CREATE TABLE IF NOT EXISTS users (
    user_id int PRIMARY KEY,
    first_name varchar NOT NULL,
    last_name varchar NOT NULL,
    gender users_gender NOT NULL,
    level membership_level NOT NULL
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id char(18) PRIMARY KEY,
    title varchar NOT NULL,
    artist_id char(18) NOT NULL,
    year int,
    duration numeric(8,5)
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id char(18) PRIMARY KEY,
    name varchar NOT NULL,
    location varchar,
    latitude numeric(7,5),
    longitude numeric(7,5)
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time timestamp PRIMARY KEY,
    hour int NOT NULL,
    day int NOT NULL,
    week int NOT NULL,
    month int NOT NULL,
    year int NOT NULL,
    weekday int NOT NULL
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
