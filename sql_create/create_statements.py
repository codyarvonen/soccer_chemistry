import sqlite3

# connection = sqlite3.connect('lineups.db')
# cursor = connection.cursor()

# cursor.execute("""DROP TABLE if exists matches;""")
# cursor.execute("""DROP TABLE if exists players;""")
# cursor.execute("""DROP TABLE if exists teams;""")
# cursor.execute("""DROP TABLE if exists lineups;""")

# cursor.execute("""CREATE TABLE matches (
#                     match_id integer not null unique, 
#                     match_link text not null, 
#                     date text not null, 
#                     home_team_id integer not null, 
#                     away_team_id integer not null, 
#                     home_team_goal integer, 
#                     away_team_goal integer,
#                     primary key (match_id)
#                 )""")

# cursor.execute("""CREATE TABLE players (
#                     player_id integer not null unique, 
#                     player_name text not null, 
#                     player_link text not null,
#                     primary key (player_id)
#                 )""")

# cursor.execute("""CREATE TABLE teams (
#                     team_id integer not null unique, 
#                     team_name text not null, 
#                     team_link text not null,
#                     primary key (team_id)
#                 )""")

# cursor.execute("""CREATE TABLE lineups (
#                     player_id integer not null, 
#                     match_id integer not null, 
#                     team_id integer not null,
#                     player_type text not null, 
#                     sub_time integer
#                 )""")

# connection.commit()
# connection.close()