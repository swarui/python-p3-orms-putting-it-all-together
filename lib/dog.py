import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    all = []
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    def save(self):
        if not self.id:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """

            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        else:
            sql = """
                UPDATE dogs 
                SET name = ?, breed = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.breed, self.id))

        CONN.commit()


    def update(self):
        self.save()
        

    @classmethod
    def create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(self):
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)

    @classmethod
    def create(cls, name, album):
        dog = cls(name, album)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        if not row:
            return None
        dog = cls(row[1], row[2])
        dog.id = row[0]

        return dog
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """

        all = CURSOR.execute(sql).fetchall()

        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs WHERE name = ?
        """

        dog = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs WHERE name = ?
        """

        dog = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM dogs WHERE id = ?
        """

        dog = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            SELECT *
            FROM dogs WHERE name = ? and breed = ?
        """

        dog = CURSOR.execute(sql, (name, breed)).fetchone()
        if dog:
            dog = cls.new_from_db(dog)
        else:
            dog = cls.create(name, breed)

        return dog