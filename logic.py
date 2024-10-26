import sqlite3
from confing import *


class DB():
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS fast_q (
                question TEXT,
                answer TEXT
            )
        ''')

            conn.execute('''
            CREATE TABLE IF NOT EXISTS q_new (
                question TEXT,
                answer TEXT,
                user_name TEXT,
                status TEXT,
                id INTEGER
            )
        ''')
            conn.execute('''
            CREATE TABLE IF NOT EXISTS worker (
                worker_name TEXT
            )
        ''')

            conn.commit()

    def get_fast_q(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM fast_q
                           """)
            
            q = [row[0] for row in cursor.fetchall()]
            return q
    def get_fast_a(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT answer FROM fast_q")
            a = [row[0] for row in cursor.fetchall()]
            return a
    def add_q(self, question, username):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT id FROM q_new
                           ORDER BY id
                           DESC
                           LIMIT 1
                           """)
            a  = [row[0] for row in cursor.fetchall()]
            cursor.execute('INSERT INTO q_new (question, answer, user_name, status,id) VALUES ( ?, ?, ?, ?, ?)',
                           (question, 'no_answer',username, 'active',int(a[0]) + 1))
    def get_q(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT question FROM q_new 
                           WHERE status = 'active'""")
            a  = [row[0] for row in cursor.fetchall()]
            return a
    def get_q_id(self,q):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM q_new WHERE question = ?", (q,))
            a  = [row[0] for row in cursor.fetchall()]
            return a[0]
    def get_id(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT id FROM q_new
                           ORDER BY id
                           """)
        a  = [row[0] for row in cursor.fetchall()]
        return a[0]
    
    def n_ans(self,id,ans):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE q_new SET answer = ?,status = ? WHERE id = ?",(ans,'inactive',id))
            conn.commit()
    def get_name_id(self,qid):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT user_name FROM q_new WHERE id = {int(qid)}")
            a  = [row[0] for row in cursor.fetchall()]
            return a[0]
    def workers(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT worker_name FROM worker""")
            a  = [row[0] for row in cursor.fetchall()]
            return a
if __name__=="__main__":
    
    m = DB(DATABASE)
    m.create_tables()
    m.get_fast_q()
    m.get_q()
    m.workers()