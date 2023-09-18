import sqlite3

from generaldb import GeneralDb


class CreditCardDb(GeneralDb):

    def final_payment(self, seat_price, client_input):
        connection = sqlite3.connect(self.db_name + ".db")
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT balance FROM {self.db_table} WHERE 
                card_number = {client_input["card_number"]} AND
                cvv = {client_input["ccv_number"]}
        """)
        try:
            result = cursor.fetchall()
        except Exception as e:
            print(e)
            connection.close()
            return False
        if result:
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
                try:
                    connection.commit()
                except Exception as e:
                    print(e)
                    connection.close()
                    return False
                connection.close()
                print("Transaction bancaire complète.")
                return True
