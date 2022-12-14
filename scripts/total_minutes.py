import sqlite3

# Returns the number of matches and minutes played for a given player
def get_total(connection:sqlite3.Connection, player_id:int):
    cursor = connection.cursor()

    results = cursor.execute("""SELECT DISTINCT match_id, player_id, player_type, sub_time
                            FROM lineups 
                            WHERE player_id = ? AND player_type != 'Bench';""", (player_id,))

    total_minutes = 0
    total_matches = 0
    for result in results:
        minutes = 0
        if result[2] == "Starter":
            minutes = 90 if result[3] is None else result[3]
        else:
            minutes = 90 - result[3] if result[3] is not None else 0
        total_minutes += minutes
        total_matches += 1

    connection.commit()

    return total_matches, total_minutes
