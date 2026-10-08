import pymysql
from config import host, user, password, db_name
#importing settings from cfg file

def get_connection(database=None):
    return pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor
    )
print("Connection approved")

def create_table(db, table, columns):
    parts = []
    for c in columns:
        parts.append(f"{c['name']} {c['type']}")
    sql = f"CREATE TABLE {table} ({', '.join(parts)})"

    connection = get_connection(db)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
        print("Table created")
    finally:
        connection.close()

def delete_table(db, table):
    sql = f"DROP TABLE `{table}`"
    connection = get_connection(db)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
        print("Table deleted")
    finally:
        connection.close()

def get_tables(db):
    connection = get_connection(db)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            rows = cursor.fetchall()
        return [list(row.values())[0] for row in rows]
    finally:
        connection.close()
def get_db():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            rows = cursor.fetchall()
        return [list(row.values())[0] for row in rows]
    finally:
        connection.close()
def get_columns(db,table):
    connection = get_connection(db)
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW COLUMNS FROM `{table}`")
            rows = cursor.fetchall()
        return rows
    finally:
        connection.close()

def insert_row(db, table, values):
    if not values:
        raise ValueError("No values provided")
    columns = ", ".join(f"`{column}`" for column in values.keys())
    placeholders = ", ".join(["%s"] * len(values))
    sql = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})"
    connection = get_connection(db)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, list(values.values()))
        connection.commit()
    finally:
        connection.close()
# def insert_row():
# def delete_row():
# def upd_row():
# def get_db():
# def get_columns():
# def select_rows():
# def check_name():

