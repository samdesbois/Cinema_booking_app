import sqlite3

from generaldb import GeneralDb


class CinemaDb(GeneralDb):

    def check_seat_availability(self, seat_choice_to_check):
        connection = sqlite3.connect(self.db_name + ".db")
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT taken FROM {self.db_table} WHERE seat_id = '{seat_choice_to_check}'
        """)
        result = cursor.fetchall()  # is a tuple into a list
        return result

    def seat_info(self, seat_choice_to_look):
        """
        Get seat data in the database.
        :param seat_choice_to_look:
        :return: tuple with 'taken' and 'price' as the only two items.
        """
        connection = sqlite3.connect(self.db_name + ".db")
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT taken, price FROM {self.db_table} WHERE 
                seat_id = '{seat_choice_to_look}'
        """)
        result = cursor.fetchall()  # is a tuple into a list
        connection.close()
        return result[0]  # is a tuple.

    def update_seat_status(self, seat_choice_to_update, id_to_update):
        connection = sqlite3.connect(self.db_name + ".db")
        cursor = connection.cursor()
        cursor.execute(f"""
            UPDATE {self.db_table} SET 
                taken = 1,  ticket_id = '{id_to_update}'
                
                WHERE seat_id = '{seat_choice_to_update}'          
        """)
        connection.commit()
        print(f"Le status du siège {seat_choice_to_update} a été mis à jour.")
