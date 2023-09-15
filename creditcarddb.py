import sqlite3

from generaldb import GeneralDb


class CreditCardDb(GeneralDb):

    def verify_card_exists(self, client_to_test):
        connection = sqlite3.connect(self.db_name + ".db")
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT * FROM {self.db_table} WHERE 
                card_number = {client_to_test["card_number"]} AND
                cvv = {client_to_test["ccv_number"]}
        """)
        result = cursor.fetchall()
        connection.close()
        return result

    def final_payment(self, seat_price, client_input):
        connection = sqlite3.connect(self.db_name + ".db")
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT balance FROM {self.db_table} WHERE 
                card_number = {client_input["card_number"]} AND
                cvv = {client_input["ccv_number"]}
        """)
        result = cursor.fetchall()
        balance = result[0][0] - seat_price
        if balance < 0:
            print("Vos fonds sont insuffisants")
            connection.close()
            return False
        else:
            cursor.execute(f"""
                UPDATE {self.db_table}
                    SET balance = {balance} WHERE
                        card_number = {client_input["card_number"]} AND
                        cvv = {client_input["ccv_number"]} 
            """)
            connection.commit()
            connection.close()
            print("Transaction bancaire complète.")
            return True
