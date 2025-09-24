from config.db_connection import get_connection

def get_airports(limits=5):
    sql = f'SELECT name FROM airport LIMIT {limits}'

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    if cursor.rowcount > 0:
        for row in result:
            print(row)
    return

get_airports(5)
