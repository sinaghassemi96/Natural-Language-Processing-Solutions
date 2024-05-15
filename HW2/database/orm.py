import psycopg2
import json


def json_formater(task):
    return {
        'name': task[1],
        'time': task[2],
        'period': task[3],
        'is_done': task[4],
        'is_cancelled': task[5]
    }


class TaskDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='nlp',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )

        self.cursor = self.conn.cursor()

        # Create a table (if it doesn't exist)
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                (id SERIAL PRIMARY KEY, name TEXT, time TEXT, date TEXT, period TEXT, done BOOLEAN, cancel BOOLEAN)''')
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)

    def create_task(self, name, time, date, period, done, cancel):
        self.cursor.execute('''INSERT INTO tasks (name, time, date, period, done, cancel) 
            VALUES (%s, %s, %s, %s, %s, %s)''', (name, time, date, period, done, cancel))
        self.conn.commit()

    def find_all(self):
        self.cursor.execute('''SELECT * FROM tasks''')
        tasks = self.cursor.fetchall()
        formatted_tasks = [json_formater(tasks) for tasks in tasks]
        return json.dumps(formatted_tasks, indent=4, ensure_ascii=False)

    def find_task(self, name):
        self.cursor.execute('''SELECT name FROM tasks WHERE name LIKE %s''', name)
        self.conn.commit()
        return self.cursor.fetchone()

    def update_user(self, task_id, time, date, done, cancel):
        self.cursor.execute("UPDATE users SET time = %s, date = %s, done = %s, cancel = %s WHERE id = %s",
                            (time, date, done, cancel, task_id))
        self.conn.commit()

    def __del__(self):
        # Close the connection
        self.cursor.close()
        self.conn.close()

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4, ensure_ascii=False)
