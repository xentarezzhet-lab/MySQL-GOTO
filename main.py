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

# def create_table(db, table, column):
#     check_name(table)
#         # columns = [{"name": "id", "type": "INT", "pk": True, "ai": True, "nn": True}, ...]
#     check_name(table)
#     parts, pks = [], []
#     for c in column:
#         check_name(c["name"])
#         if c["type"] not in ALLOWED_TYPES:      
#             raise ValueError(f"Недопустимый тип: {c['type']}")
#         line = f"`{c['name']}` {c['type']}"
#         if c["nn"] or c["pk"]:
#             line += " NOT NULL"
#         if c["ai"]:
#             line += " AUTO_INCREMENT"
#         parts.append(line)
#         if c["pk"]:
#             pks.append(f"`{c['name']}`")
#     if pks:
#         parts.append(f"PRIMARY KEY ({', '.join(pks)})")

#     sql = f"CREATE TABLE `{table}` ({', '.join(parts)})"
#     connection = get_connection(db)
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(sql)                 
#         connection.commit()
#     finally:
#         connection.close()


# def insert_row():
#         # data = {"column name": meaning}; empty string becomes None -> NULL
#     if not data:
#         raise ValueError("Нет данных для вставки")
#     names = ", ".join(f"`{k}`" for k in data)
#     placeholders = ", ".join(["%s"] * len(data))
#     values = [(v if v != "" else None) for v in data.values()]

#     sql = f"INSERT INTO `{table}` ({names}) VALUES ({placeholders})"
#     connection = get_connection(db)
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(sql, values)         
#             new_id = cursor.lastrowid
#         connection.commit()
#         return new_id
#     finally:
#         connection.close()
# def delete_row():

# def delete_table():
# def upd_row():
# def get_db():
# def get_table():
# def get_columns():
# def select_rows():
# def check_name(): #check on user input name 
#     if not isinstance(name, str) or len(name) > 64:
#         raise ValueError("Name should be str not longer than 64")
#     if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
#         raise ValueError(f"Incorrect name: '{name}' (num??)")
