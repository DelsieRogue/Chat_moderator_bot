import sqlite3

conn = sqlite3.connect('tBot.db')
cur = conn.cursor()


def add_user_to_table_users(user_id, username, role_name, fn="", ln=""):
    cur.execute(f"""SELECT role_id FROM roles WHERE role_name="{role_name}" """)
    res = cur.fetchone()[0]
    cur.execute(f"""INSERT INTO users (user_id, username, firstname, lastname, role_id)
     VALUES ({user_id}, "{username}", "{fn}", "{ln}", {res});""")
    conn.commit()


def add_order_to_table_orders(user_id, is_admin=False):
    cur.execute(f"""INSERT INTO orders (user_id, end_date)
     VALUES ({user_id}, 
        {"null" if is_admin else "(DATETIME((datetime('now','localtime')), '+1 months'))"}
        );""")
    conn.commit()


def add_role_to_table_roles(role_name):
    cur.execute(f"""INSERT INTO roles (role_name)
     VALUES ("{role_name}");""")
    conn.commit()


def drop_table(table):
    cur.execute(f"""DROP TABLE {table};""")
    conn.commit()


def create_table_users():
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY NOT NULL,
        username VARCHAR(75) NOT NULL UNIQUE,
        firstname VARCHAR(75),
        lastname VARCHAR(75),
        role_id INTEGER NOT NULL,
        begin_date datetime DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (role_id) REFERENCES roles(roles_id)
        );""")
    conn.commit()


def create_tabel_roles():
    cur.execute("""CREATE TABLE IF NOT EXISTS roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,        
        role_name VARCHAR(25) NOT NULL UNIQUE
        );""")
    conn.commit()


def create_table_order():
    cur.execute("""CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        begin_date datetime DEFAULT (datetime('now','localtime')),
        end_date datetime
        );""")
    conn.commit()


def get_users_from_db(roles):
    roles_for_query = str(roles)[1:-1]
    return cur.execute(f"""SELECT u.username, strftime('%d.%m.%Y', max(o.end_date)) FROM users u
                    LEFT JOIN roles  r ON u.role_id=r.role_id LEFT JOIN orders o ON u.user_id =o.user_id 
                    WHERE r.role_name IN ({roles_for_query}) GROUP BY u.username""").fetchall()


def get_role(user_id):
    return cur.execute(f"""SELECT r.role_name FROM (SELECT * FROM users us WHERE us.user_id={user_id}) u 
    LEFT JOIN roles r ON r.role_id=u.role_id""").fetchone()


def set_role(user_id, to_role_name):
    cur.execute(f"""UPDATE users SET role_id=(SELECT role_id from roles WHERE role_name='{to_role_name}') 
    WHERE user_id={user_id}""")
    add_order_to_table_orders(user_id)
