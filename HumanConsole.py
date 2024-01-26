import spacy
import webbrowser
import os
import subprocess


def execute_command(command):
    doc = nlp(command)
    order_word = ""
    order_object = ""
    lemma_command = ""
    run_word = ["uruchom", "otwórz"]

    i = 0
    for token in doc:
        if token.pos_ == "VERB" and i < 1:
            order_word = token.text.lower()
            i = 1
        elif token.tag_ == "SUBST" and token.text != "program" and token.text != "dokument":
            order_object = token.text

    if len(order_object) == 0:
        order_object = command.split(" ")[-1]

    elif len(command.split(" ")) > 3:
        for token in doc:
            if token.text != order_object:
                lemma_command += token.lemma_ + " "

    program_name = order_object

    if order_word in run_word and "program" in command:
        if program_name:
            try:
                os.system(f"start {program_name}")
                print(f"Uruchomiono program: {program_name}")
            except Exception as e:
                print(f"Błąd podczas uruchamiania programu {program_name}: {e}")

    elif "zamknij" == order_word and "program" in command:
        if program_name:
            try:
                subprocess.check_call(["taskkill", "/f", "/im", program_name + ".exe"])
                print(f"Zamknięto program: {program_name}")
            except subprocess.CalledProcessError:
                print(f"Błąd podczas zamykania programu: {program_name}")
            return

    elif order_word in run_word and "dokument" in command:
        if order_object:
            file_path = order_object
            try:
                os.startfile(file_path)
                print(f"Otwarto plik: {file_path}")
            except FileNotFoundError:
                print(f"Nie można znaleźć pliku: {file_path}")
            return

    elif order_word in run_word and "strona" in lemma_command and "internetowy" in lemma_command:
        if order_object:
            website_name = order_object
            webbrowser.open(website_name)
        return

    else:
        print("Nie rozpoznano polecenia.")
        return


nlp = spacy.load("pl_core_news_sm")
print("""Program Ludzka Konsola:
Wpisz:
- aby uruchomić program: Uruchom program nazwa_programu
- aby zamknąć program: Zamknij program nazwa_programu
- aby otworzyć dokument: Otwórz dokument ścieżka_do_pliku
- aby otworzyć w przeglądarce stronę internetową: Otwórz stronę internetową adres_strony
- aby wyjść z programu: exit
""")
while True:
    user_input = input("Wprowadź polecenie: ")
    if user_input.lower() == "exit":
        break
    execute_command(user_input)
