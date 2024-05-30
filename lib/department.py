import sqlite3

CONN = sqlite3.connect('database.db')
CURSOR = CONN.cursor()

class Department:
    all = {}

    def __init__(self, name, location, id=None):
        self.name = name
        self.location = location
        self.id = id

    @classmethod
    def create_table(cls):
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                location TEXT
            )
        ''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS departments")
        CONN.commit()

    def save(self):
        if not self.id:
            CURSOR.execute("INSERT INTO departments (name, location) VALUES (?, ?)",
                           (self.name, self.location))
            self.id = CURSOR.lastrowid
        else:
            CURSOR.execute("UPDATE departments SET name = ?, location = ? WHERE id = ?",
                           (self.name, self.location, self.id))
        CONN.commit()
        type(self).all[self.id] = self

    def delete(self):
        CURSOR.execute("DELETE FROM departments WHERE id = ?", (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        department = cls.all.get(row[0])
        if department:
            department.name = row[1]
            department.location = row[2]
        else:
            department = cls(row[1], row[2], row[0])
            cls.all[department.id] = department
        return department

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM departments")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM departments WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM departments WHERE name = ?", (name,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    def employees(self):
        from employee import Employee
        CURSOR.execute("SELECT * FROM employees WHERE department_id = ?", (self.id,))
        rows = CURSOR.fetchall()
        return [Employee.instance_from_db(row) for row in rows]