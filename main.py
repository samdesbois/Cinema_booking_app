import os
import yagmail
from fpdf import FPDF
from random import sample
import string

from cinemadb import CinemaDb
from creditcarddb import CreditCardDb


def send_pdf_by_email(client_entered, seat_choice_entered , id_created):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, "E-TICKET")
    pdf.ln(20)
    pdf.cell(40, 10, f"Nom du client : "
                     f"{client_entered['full_name']}")
    pdf.ln(20)
    pdf.cell(40, 10, f"Siège : "
                     f" {seat_choice_entered}")
    pdf.ln(20)
    pdf.cell(40, 10, f"Ticked id : "
                     f" {id_created}")
    file_path = "files/" + \
                "_".join(client_entered['full_name'].lower().split()) + \
                "_ticket.pdf"
    pdf.output(file_path)
    print("fichier pdf créé.")
    yag = yagmail.SMTP('julien.samson',
                       'trqoawghgnjdhjkd')
    contents = [
        'Encore merci pour votre achat.',
        'Ci-joint votre e-ticket.',
        'Cordialement']
    yag.send(client_entered["email"],
             'Test',
             contents,
             attachments=[f'{file_path}'])
    print("Email envoyé!")
    os.remove(file_path)
    print(f"Fichier {file_path} effacé.")


def generate_random_ticket_id():
    """
    Generate a random string
    :param number:
    :return:
    """
    string_base = string.printable
    char_to_remove = (" ", '"')
    for c in char_to_remove:
        string_base = string_base.replace(c, "")
    id_length = 10
    id_result = ''.join(sample(string_base, id_length))
    return id_result


if __name__ == '__main__':
    print("Bienvenue à la billetterie en ligne.")

    # Create instance
    cinema_db = CinemaDb("cinema", "Seat")
    # Verify databases and create them if needed.
    if not cinema_db.check_database_availability():
        cinema_db.create_file()
        cinema_db.create_table({
            "seat_id": "TEXT",
            "taken": "INTEGER",
            "price": "INTEGER",
            "ticket_id": "TEXT"
        })
        cinema_db.insert_into_table(
            ["A1", 0, 100, ""],
            ["A2", 0, 90, ""],
            ["B1", 0, 120, ""],
            ["B2", 1, 140, ""]
        )

    # Create instance
    card_db = CreditCardDb("credit_card", "Card")
    # Verify databases and create them if needed.
    if not card_db.check_database_availability():
        card_db.create_file()
        card_db.create_table({
            "full_NAME": "TEXT",
            "card_brand": "TEXT",
            "card_number": "INTEGER",
            "cvv": "INTEGER",
            "balance": "INTEGER"
        })
        card_db.insert_into_table(
            ["Molly Little", "Mastercard", 5104287118333464, 932, 2000],
            ["Sean Klein", "Mastercard", 51019144731757292, 390, 50],
            ["Gerard Tillman", "Visa", 4500740792612440, 365, 735]
        )

    while True:
        initial_response = input("Voulez-vous choisir un (autre) siège? (Y/n)")
        if initial_response.lower() != "y" and initial_response != "":
            break
        else:
            seat_choice = input("Merci de choisir un siège : ")
            if cinema_db.check_seat_availability(seat_choice):
                pass
            else:
                print("Ce siège est déjà pris :(")
                continue
            print(f"Prix du siège {seat_choice}: "
                  f"{cinema_db.seat_info(seat_choice)[1]} €.")
            response = input("Voulez-vous réserver ce siège ? (Y/n) : ")
            if response.lower() != "y" and response != "":
                continue
            else:
                client = dict()
                client["full_name"] = input("Merci d'écrire "
                                            "votre nom complet : ")
                try:
                    client["card_number"] = int(
                        input(f"{client['full_name']}, "
                              "entrez maintenant "
                              "votre numéro de carte "
                              "bleue : "))
                except:
                    print("Invalid card number")
                    continue
                try:
                    client["ccv_number"] = int(input(f"Please now add a the "
                                                     f"CCV code behind your "
                                                     f"card : "))
                except:
                    print("Invalid CCV number")
                    continue
                print(f"Thank you {client['full_name']} for all this infos.")
                response = input("Please confirm to finalise "
                                 "your command! (Y/n)")
                if response.lower() != "y" and response != "":
                    continue
                else:
                    if card_db.final_payment(
                            cinema_db.seat_info(seat_choice)[1],
                            client
                    ):
                        ticket_id = generate_random_ticket_id()
                        cinema_db.update_seat_status(seat_choice, ticket_id)
                        print(f"Merci pour votre achat"
                              f" {client['full_name']}.")
                        print(f"Vous avez donc réservé le siège"
                              f" {seat_choice} avec l'id : {ticket_id}")
                        email_response = input("Voulez-vous recevoir"
                                               " par email ? (Y/n)")
                        if email_response.lower() != "y" and email_response != "":
                            pass
                        else:
                            client["email"] = input("Votre email : ")
                            send_pdf_by_email(
                                client,
                                seat_choice,
                                ticket_id
                            )
                    else:
                        print("An error occurred, please verify you credit "
                              "card infos.")
                        continue

    print("Merci pour votre venue")
