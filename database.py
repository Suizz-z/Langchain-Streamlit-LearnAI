import sqlite3
from datetime import datetime, timedelta
import json
import pandas as pd

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_history (
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            question TEXT NOT NULL,
            PRIMARY KEY (user_id, date),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_massage_history (
            user_id INTEGER NOT NULL,
            session_id TEXT NOT NULL,
            message TEXT NOT NULL,
            PRIMARY KEY (user_id, session_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tree_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tree_name TEXT NOT NULL,
            tree_data TEXT NOT NULL,
            tree_node_properties TEXT NOT NULL, 
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE (user_id, tree_name) 
        );
    ''')

    conn.commit()
    conn.close()

def add_user(username, password, email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password, email)
            VALUES (?, ?, ?)
        ''', (username, password, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def add_user_question(user_id, date, question):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO user_history (user_id, date, question)
            VALUES (?, ?, ?)
        ''', (user_id, date, question))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error adding user history: {e}")
        return False
    finally:
        conn.close()

def check_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
         SELECT id, username FROM users WHERE username = ? AND password = ?
    ''', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user
def get_user_history_times(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT date FROM user_history WHERE user_id = ?
    ''', (user_id,))
    times = cursor.fetchall()
    conn.close()
    return [time[0] for time in times]
def get_user_history(user_id, date_time):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT date, question FROM user_history WHERE user_id = ? AND date LIKE ?
    ''', (user_id, f"{date_time}%"))
    history = cursor.fetchall()
    conn.close()
    return history


def get_last_two_days_history(user_id):
    all_times = get_user_history_times(user_id)

    sorted_times = sorted([datetime.strptime(time, '%Y-%m-%d %H:%M') for time in all_times], reverse=True)

    last_two_days = sorted_times[:2]

    last_two_days_str = [time.strftime('%Y-%m-%d') for time in last_two_days]

    history = []
    for date_time in last_two_days_str:
        history.extend(get_user_history(user_id, date_time))

    return history
def get_chat_ids(user_id):
    conn = sqlite3.connect('message_history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT session_id FROM message_store WHERE session_id LIKE ?", (f"{user_id}%",))
    chat_ids = [row[0].split('+')[1] for row in cursor.fetchall()]  # 只取+后面的部分
    conn.close()
    return list(set(chat_ids))
def save_tree_data(user_id, tree_name, tree_data, tree_node_properties):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    df_json = tree_data.to_json(orient='records')
    node_properties_json = json.dumps(tree_node_properties)

    try:
        cursor.execute('''
            INSERT INTO tree_data (user_id, tree_name, tree_data, tree_node_properties)
            VALUES (?, ?, ?, ?)
        ''', (user_id, tree_name, df_json, node_properties_json))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Tree with this name already exists for the user.")
    finally:
        conn.close()
def load_tree_data(user_id, tree_name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT tree_data, tree_node_properties 
        FROM tree_data 
        WHERE user_id = ? AND tree_name = ?
    ''', (user_id, tree_name))
    result = cursor.fetchone()

    if result:
        tree_data = result[0]
        tree_node_properties = result[1]
        df = pd.read_json(tree_data)
        node_properties = json.loads(tree_node_properties)
        conn.close()
        return df, node_properties
    else:
        conn.close()
        return None, None
def update_tree_node_properties(user_id, tree_name, new_properties):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    node_properties_json = json.dumps(new_properties)
    update_query = """
    UPDATE tree_data
    SET tree_node_properties = ?
    WHERE user_id = ? AND tree_name = ?
    """
    cursor.execute(update_query, (node_properties_json, user_id, tree_name))
    conn.commit()  # 提交事务

def get_second_level_nodes(user_id,tree_name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT tree_data
        FROM tree_data 
        WHERE user_id = ? AND tree_name = ?
    ''', (user_id, tree_name))
    result = cursor.fetchone()
    if not result:
        return None
    nodes_data = json.loads(result[0])

    if result:
        return nodes_data