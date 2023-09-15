import os
import sqlite3


class GeneralDb:

    def __init__(self, db_name, db_table):
        self.db_name = db_name
        self.db_table = db_table

    def check_database_availability(self):
        print(f"Checking {self.db_name} db...")
        if not os.path.exists(self.db_name + ".db"):
            print("Initial db doesn't exit. A new one will be created...")
            return False
        else:
            print("db file already exists.")
            return True

    def create_file(self):
        file = open(self.db_name + ".db", "a")
        file.close()
        print(f"File {self.db_name}.db was created.")

    def create_table(self, db_structure):
        """
        Create table with specific parameters.

        :param db_name: string
        :param db_structure: dictionary
        :return: nothing
        """
        connexion = sqlite3.connect(self.db_name + ".db")
        structure_list = list()
        for key, value in db_structure.items():
            structure_list.append(f"{key} {value}")
        structure_string = ",".join(structure_list)
        connexion.execute(f"""
            CREATE TABLE {self.db_table} ({structure_string})
            """)
        connexion.commit()
        connexion.close()
        print(f"{self.db_table} table was created")

    def insert_into_table(self, *list_values):
        connection = sqlite3.connect(self.db_name + ".db")
        cursor = connection.execute(f"""
            SELECT * from {self.db_table}
        """)
        columns_str = ", ".join(
            list(description[0] for description in cursor.description)
        )
        for p in list_values:
            p = ['"' + i + '"' if type(i) == str else i for i in p]
            p = [str(i) for i in p]
            value_str = str(", ".join(p))
            sql_command = f"INSERT INTO {self.db_table} ({columns_str}) VALUES({value_str})"
            connection.execute(sql_command)
        connection.commit()
        connection.close()
        print(f"{list_values} were inserted in {self.db_table} with success.")
