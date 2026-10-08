import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from config import db_name
from main import get_tables, create_table, delete_table, get_db

TYPES = ["INT", "VARCHAR(45)", "VARCHAR(100)", "DECIMAL(8,2)", "DATE", "DATETIME"]

root = tk.Tk()
root.title("MySQL GOTO")

def current_db():
    return combo_db.get()
# ---------- DB SELECTION! ----------
tk.Label(root, text="База:").grid(row=0, column=0, padx=10, pady=10)
combo_db = ttk.Combobox(root, state="readonly", width=30)
combo_db.grid(row=0, column=1, padx=10)

# ---------- table selection! ----------
tk.Label(root, text="Table:").grid(row=1, column=0, padx=10, pady=10)
combo = ttk.Combobox(root, state="readonly", width=30)
combo.grid(row=1, column=1, padx=10)

def refresh_db():
    try:
        combo_db["values"] = get_db()
    except pymysql.MySQLError as e:
        messagebox.showerror("DB Error", str(e))
        return
    combo_db.set(db_name)
    refresh_tables()

def refresh_tables():
    if not current_db():
        combo["values"] = []
        combo.set("")
        return
    # re-read the list of tables from the database and update the drop-down list
    try:
        combo["values"] = get_tables(current_db())
    except pymysql.MySQLError as e:
        messagebox.showerror("DB Error", str(e))
    combo.set("")  # clear selection

combo_db.bind("<<ComboboxSelected>>", lambda event: refresh_tables())
# ---------- delete here! ----------
def on_delete_click():
    table = combo.get()
    if not table:
        messagebox.showwarning("Attention", "First select a table")
        return
    if not messagebox.askyesno("Deleting", f"Delete table {table} with all data?"):
        return
    try:
        delete_table(current_db(), table)
    except pymysql.MySQLError as e:
        messagebox.showerror("DB Error", str(e))
        return
    messagebox.showinfo("Succesed", f"Table {table} deleted")
    refresh_tables()


# ---------- create pop up window! ----------
def open_create_window():
    win = tk.Toplevel(root)
    win.title("Create table")

    tk.Label(win, text="Table name:").grid(row=0, column=0, padx=10, pady=10)
    entry_name = tk.Entry(win, width=25)
    entry_name.grid(row=0, column=1, columnspan=2)

    rows_frame = tk.Frame(win)  
    rows_frame.grid(row=1, column=0, columnspan=3, padx=10)
    col_rows = [] 

    def add_row():
        r = len(col_rows)
        e = tk.Entry(rows_frame, width=18)
        t = ttk.Combobox(rows_frame, values=TYPES, state="readonly", width=14)
        t.current(0)
        e.grid(row=r, column=0, padx=3, pady=2)
        t.grid(row=r, column=1, padx=3)
        col_rows.append((e, t))

    def on_create_click():
        columns = [{"name": e.get().strip(), "type": t.get()}
                   for e, t in col_rows if e.get().strip()]
        table = entry_name.get().strip()
        if not table or not columns:
            messagebox.showwarning("Warning", "Specify the table name and at least one column.")
            return
        try:
            create_table(current_db(), table, columns)
        except pymysql.MySQLError as e:
            messagebox.showerror("DB Error", str(e))
            return
        messagebox.showinfo("Succesful", f"Table {table} was made")
        refresh_tables()
        win.destroy()

    add_row()  
    tk.Button(win, text="+ column", command=add_row).grid(row=2, column=0, pady=10)
    tk.Button(win, text="Create", command=on_create_click).grid(row=2, column=1, pady=10)


# ---------- main window buttons! ----------
tk.Button(root, text="Reload DBS", command=refresh_db).grid(row=0, column=2, padx=5)
tk.Button(root, text="Create table", command=open_create_window).grid(row=2, column=0, columnspan=2, pady=5)
tk.Button(root, text="Delete table", command=on_delete_click).grid(row=3, column=0, columnspan=2, pady=5)

refresh_db()# refresh everything
root.mainloop()