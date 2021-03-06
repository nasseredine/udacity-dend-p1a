import os
import glob
import math
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """Process log files located under a given filepath.
    
    Transforms and loads song data and artist data in songs and artists tables respectively.
    
    Args:
        cur (cursor): The `cursor` object to the database session (from psycopg2).
        filepath (str): The filepath of song data to be processed.
    
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    year = song_data[3]
    song_data[3] = None if not year else year # replace year with None if 0
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    location = artist_data[2]
    latitude = artist_data[3]
    longitude = artist_data[4]
    artist_data[2] = None if not location else location # replace location with None if ''
    artist_data[3] = None if math.isnan(latitude) else latitude # replace latitude with None if nan
    artist_data[4] = None if math.isnan(longitude) else longitude # replace longitude with None if nan
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """Process log files located under a given filepath.
    
    Transforms and loads time data, user and songplay data in time, users and songplays tables respectively.
    
    Args:
        cur (cursor): The `cursor` object to the database session (from psycopg2).
        filepath (str): The filepath of log data to be processed.
    
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df.page == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts, unit='ms')
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        song_id, artist_id = results if results else (None, None)

        # insert songplay record
        songplay_data = (t[index], row.userId, row.level, song_id, artist_id, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Process data files located under a given filepath using a given function.
    
    Args:
        cur (cursor): The `cursor` object to the database session (from psycopg2).
        conn (connection): The `connection` object to the database (from psycopg2).
        filepath (str): The filepath of data to be processed.
        func (function): The `function` to process the data files with.
        
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """Connects to the local sparkifydb and process song and log data."""
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()