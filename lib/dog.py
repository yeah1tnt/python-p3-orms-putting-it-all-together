import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)


    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.lastrowid
    
    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls,row):
        return cls(row[1], row[2], row[0])
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """
        return [cls.new_from_db(row) for row in CURSOR.execute(sql).fetchall()]
    
    @classmethod
    def find_by_name(cls,name):
        sql = """
            SELECT * FROM dogs
            WHERE name = ?
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        if not dog:
            return None
        return cls.new_from_db(dog)
    @classmethod
    def find_by_id(cls,id):
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
        """
        return cls.new_from_db(CURSOR.execute(sql, (id,)).fetchone())
    
    @classmethod
    def find_or_create_by(cls, name=None, breed=None):
        sql = """
            SELECT * FROM dogs
            WHERE (name, breed) = (?, ?)
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name, breed)).fetchone()
        if not dog:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (name, breed))
            return Dog(
                name=name,
                breed=breed,
                id=CURSOR.lastrowid  
            )
        return cls.new_from_db(dog)
    
    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?, breed = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))