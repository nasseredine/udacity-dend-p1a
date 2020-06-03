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
    songplay_id serial PRIMARY KEY,
    start_time timestamp NOT NULL,
    user_id int NOT NULL,
    level membership_level NOT NULL,
    song_id char(18),
    artist_id char(18),
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
    duration numeric(8,5) NOT NULL
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id char(18) PRIMARY KEY,
    name varchar NOT NULL,
    location varchar,
    latitude numeric(8,5),
    longitude numeric(8,5)
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
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
""")


time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
""")

# FIND SONGS

song_select = ("""
SELECT song_id, artist_id
FROM songs
JOIN artists USING (artist_id)
WHERE title = %s AND name = %s AND duration = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
