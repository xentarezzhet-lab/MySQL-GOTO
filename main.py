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
        cursorclass=pymysql.cursors.DictCursor,
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
if __name__ == "__main__":
    cols = [{"name": "id", "type": "INT"}, {"name": "fio", "type": "VARCHAR(100)"}]
    create_table(db_name, "test_table", cols)





# def insert_row():
# def delete_row():

# def delete_table():
# def upd_row():
# def get_db():
# def get_table():
# def get_columns():
# def select_rows():
# def check_name():

