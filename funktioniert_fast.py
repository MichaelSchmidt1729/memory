import tkinter as tk
from PIL import Image, ImageTk
import os
import random
import time
import unidecode

class SimilarityCheck:
    @staticmethod
    def normalize_text(text):
        replacements = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
                        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue'}
        for original, replacement in replacements.items():
            text = text.replace(original, replacement)

        return unidecode.unidecode(text).lower()

    @staticmethod
    def check_similarity(input_name, folder_name):
        # Normalisiere die Eingabe und den Ordnername
        input_name_normalized = SimilarityCheck.normalize_text(input_name)
        folder_name_normalized = SimilarityCheck.normalize_text(folder_name)

        # Überprüfe auf Ähnlichkeit
        return input_name_normalized == folder_name_normalized

    @staticmethod
    def check_guess(folder_name, guess):
        last_name, first_name = folder_name.split('-')
        guess_parts = guess.split()

        results = {'first_name': False, 'last_name': False}
        for part in guess_parts:
            if SimilarityCheck.check_similarity(part, first_name):
                results['first_name'] = True
            elif SimilarityCheck.check_similarity(part, last_name):
                results['last_name'] = True

        return results
    
class GiveHint:
    def __init__(self, statistics):
        self.first_name_hint_index = 0
        self.last_name_hint_index = 0
        self.statistics = statistics

    def get_first_name_hint(self, first_name, full_name):
        if self.first_name_hint_index < len(first_name):
            hint = first_name[:self.first_name_hint_index + 1]
            self.first_name_hint_index += 1
            self.statistics.add_hinted_person(full_name)  # Add the person to hinted persons list
            return hint
        return first_name

    def get_last_name_hint(self, last_name, full_name):
        if self.last_name_hint_index < len(last_name):
            hint = last_name[:self.last_name_hint_index + 1]
            self.last_name_hint_index += 1
            self.statistics.add_hinted_person(full_name)  # Add the person to hinted persons list
            return hint
        return last_name

    def reset_hints(self):
        self.first_name_hint_index = 0
        self.last_name_hint_index = 0

class MyStatistics:
    def __init__(self):
        self.total_correct = 0
        self.total_incorrect = 0
        self.first_name_correct = 0
        self.last_name_correct = 0
        self.first_name_incorrect = 0
        self.last_name_incorrect = 0
        self.hints_given = 0
        self.hinted_persons = {}
        self.start_time = time.time()
        self.total_rounds = 0

    def add_hinted_person(self, name):
        if name in self.hinted_persons:
            self.hinted_persons[name] += 1
        else:
            self.hinted_persons[name] = 1

    def prepare_labels(self):
        self.labels = []
        self.calculate_statistics()
        self.compose_labels()

    def calculate_statistics(self):
        self.elapsed_time = time.time() - self.start_time
        self.total_possible_persons = len(os.listdir("C:/Users/Michael Schmidt/OneDrive - SeitWerk GmbH/Dokumente/Python Scripts/Memory/MABilder"))
        self.total_rounds = self.total_correct + self.total_incorrect
        self.calculate_percentage()

    def calculate_percentage(self):
    # Berechnungen für Statistiken
        self.correct_percentage = round(self.total_correct / self.total_rounds * 100, 1) if self.total_rounds > 0 else 0
        self.incorrect_percentage = round(self.total_incorrect / self.total_rounds * 100, 1) if self.total_rounds > 0 else 0
        self.persons_percentage = round(self.total_rounds / self.total_possible_persons * 100, 1) if self.total_possible_persons > 0 else 0
        self.average_time_per_correct_guess = (self.elapsed_time / self.total_correct) if self.total_correct > 0 else 0
        self.total_first_names = self.first_name_correct + self.first_name_incorrect
        self.total_last_names = self.last_name_correct + self.last_name_incorrect
        self.first_name_correct_percentage = round(self.first_name_correct / self.total_first_names * 100, 1) if self.total_first_names > 0 else 0
        self.first_name_incorrect_percentage = round(self.first_name_incorrect / self.total_first_names * 100, 1) if self.total_first_names > 0 else 0
        self.last_name_correct_percentage = round(self.last_name_correct / self.total_last_names * 100, 1) if self.total_last_names > 0 else 0
        self.last_name_incorrect_percentage = round(self.last_name_incorrect / self.total_last_names * 100, 1) if self.total_last_names > 0 else 0        

    def compose_labels(self):
        self.labels = [
        f"Als Runde gilt:\nDie Person wurde korrekt erkannt, 'Lösen' gewählt, oder \n{Memory.MAX_ERRORS} Fehlversuche wurden eingegeben",
        f"Gespielte Runden: {self.total_rounds}",
        f"Gelöste Runden: {self.total_correct} ({self.correct_percentage:.2f}%)",
        f"Ungelöste Runden: {self.total_incorrect} ({self.incorrect_percentage:.2f}%)",
        "────────────────────────────",
        f"Über alle Runden hinweg:",
        f"Anzahl insgesamt richtig getippter Vornamen: {self.first_name_correct} ({self.first_name_correct_percentage:.2f}%)",
        f"Anzahl insgesamt falsch getippter Vornamen: {self.first_name_incorrect} ({self.first_name_incorrect_percentage:.2f}%)",
        f"Anzahl insgesamt richtig getippter Nachnamen: {self.last_name_correct} ({self.last_name_correct_percentage:.2f}%)",
        f"Anzahl insgesamt falsch getippter Nachnamen: {self.last_name_incorrect} ({self.last_name_incorrect_percentage:.2f}%)",
        "────────────────────────────",
        f"Gesamtzahl möglicher Personen: {self.total_possible_persons}",
        f"Prozentsatz an davon getippten Personen: {self.persons_percentage:.2f}%",
        f"Spielzeit: {self.elapsed_time / 60:.2f} Minuten",
        "────────────────────────────",
        ]     
        self.append_average_time_per_correct_guess()   
        self.append_hints_info()

    def append_average_time_per_correct_guess(self):
        if self.total_correct > 0:
            self.average_time_per_correct_guess = self.elapsed_time / self.total_correct
            self.labels.append(f"Ø Zeit bis zu einer Lösung: {self.average_time_per_correct_guess / 60:.2f} Minuten")
        else:
            self.labels.append("Ø Zeit bis zu einer Lösung: 0 Namen korrekt gelöst")

    def append_hints_info(self):
        if self.hints_given > 0:
            hints_info = ["Anzahl der gegebenen Hinweise: " + str(self.hints_given)]
            for name, count in self.hinted_persons.items():
                hints_info.append(f"{name} (x{count} mal)")
            hints_text = "\n".join(hints_info)
            self.labels.append(hints_text)

    def show_statistics(self):
        self.prepare_labels()
        self.create_statistics_window()

    def create_statistics_window(self):
        self.stats_window = tk.Tk()
        self.stats_window.title("Spielstatistik")
        self.determine_window_size()

        # Erstelle ein Text-Widget für die gesamten Statistiken
        self.stats_text = tk.Text(self.stats_window, wrap='word', font=("Arial", 10), exportselection=True, spacing1=4)
        
        # Füge alle Statistik-Texte zum Text-Widget hinzu
        self.populate_statistics_window()

        # Konfiguriere das Text-Widget, damit es nur zum Lesen ist
        self.stats_text.config(state=tk.DISABLED, bg=self.stats_window.cget('bg'))
        
        # Füge Scrollbar hinzu, falls benötigt
        scrollbar = tk.Scrollbar(self.stats_window, command=self.stats_text.yview)
        self.stats_text['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.stats_text.pack(expand=True, fill='both', padx=10, pady=10)
        self.stats_window.mainloop()

    def determine_window_size(self):
        # Annahme einer durchschnittlichen Zeilenhöhe für die Berechnung
        label_height = 25  
        self.window_height = len(self.labels) * label_height + 50  # Zusätzlicher Platz für Fensterränder und Abstände
        self.window_width = 400
        self.stats_window.minsize(340, 0)
        self.stats_window.geometry(f"{self.window_width}x{self.window_height}")  # Dynamische Fenstergröße

    def populate_statistics_window(self):
        self.prepare_labels()

      # Füge alle Statistik-Texte zum Text-Widget hinzu
        for line in self.labels:
            self.stats_text.insert(tk.END, line + '\n')            

class Memory:
    MAX_ERRORS = 5  # Maximale Anzahl an Fehlversuchen
    IMAGES_FOLDER = "C:/Users/Michael Schmidt/OneDrive - SeitWerk GmbH/Dokumente/Python Scripts/Memory/MABilder"  # Pfad zum Bildordner, in dem die Unterordner liegen. Die Unterordner heißen nachname-vorname, die Bilder darin enthalten "funny" oder "normal"
    WAIT_TIME_BEFORE_NEXT = 700  # Wartezeit in Millisekunden vor dem Laden der nächsten Person

    def __init__(self):
        # Initialisieren der grafischen Benutzeroberfläche
        self.root = tk.Tk()
        self.root.geometry("400x500")
        self.root.title("Memory-Spiel")
        
        self.current_folder = ""
        self.statistics = MyStatistics()
        self.hint_giver = GiveHint(self.statistics)

        self.first_name_only = tk.BooleanVar(value=False)  # Checkbox für "Vorname reicht aus" initialisieren

        self.setup_ui()

        self.guessed_folders = []
        self.error_count = 0
        self.current_tip_count = 1  # Neue Variable für die Anzahl der Tipps für die aktuelle Person

        self.load_next_image()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)



    def setup_ui(self):
        # Checkbox für "Vorname reicht aus" direkt unter der Titelleiste
        self.first_name_checkbox = tk.Checkbutton(self.root, text="Vorname reicht aus", variable=self.first_name_only)
        self.first_name_checkbox.pack()  # Positionieren direkt unter der Titelleiste

        # Rundenlabel
        self.round_label = tk.Label(self.root, text="Runde 1")
        self.round_label.pack()

        # Bildlabel
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Outputlabel für Benutzerfeedback
        self.output_label = tk.Label(self.root, text="Bitte Vor- und Nachnamen eingeben und mit Enter bestätigen") 
        self.output_label.pack()

        # Eingabefeld für Benutzereingaben
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack()
        self.entry.bind("<Return>", self.on_submit)

        # Button zum Lösen der aktuellen Aufgabe
        self.solve_button = tk.Button(self.root, text="Lösen", command=self.solve_guess)
        self.solve_button.pack()

        # Button für Hinweise auf den Vornamen
        self.hint_first_name_button = tk.Button(self.root, text="Tipp Vorname", command=self.hint_first_name)
        self.hint_first_name_button.pack()

        # Button für Hinweise auf den Nachnamen
        self.hint_last_name_button = tk.Button(self.root, text="Tipp Nachname", command=self.hint_last_name)
        self.hint_last_name_button.pack()

    def check_name_part(self, guess_part, correct_part, part_type):
        is_correct = SimilarityCheck.check_similarity(guess_part, correct_part)
        has_typo = False if is_correct else SimilarityCheck.check_typo_similarity(guess_part, correct_part) # Überprüft, ob ein Teil des Namens (Vorname oder Nachname) korrekt ist. Gibt ein Tuple zurück: (is_correct, has_typo)
        if has_typo:
            self.output_label.config(text=f"Achtung: Buchstabendreher im {part_type}!")
        return is_correct, has_typo

    def on_submit(self, event=None):
        guess = self.entry.get().strip()  # Entfernen von Leerzeichen am Anfang und Ende
        self.current_tip_count += 1  # Zählt die Anzahl der Tipps für die aktuelle Person
        self.update_round_label()  # Aktualisiert die Anzeige für die Runde und Tipp-Anzahl
 
        if not guess:
            last_name, first_name = self.current_folder.split('-')
            self.output_label.config(text=f"Name: {first_name} {last_name}")
            self.root.after(Memory.WAIT_TIME_BEFORE_NEXT, self.load_next_image)  # Warte WAIT_TIME_BEFORE_NEXT und lade dann das nächste Bild
            return

        results = SimilarityCheck.check_guess(self.current_folder, guess)

        first_name_feedback = "Vorname ✓" if results['first_name'] else "Vorname ✗"
        last_name_feedback = "Nachname ✓" if results['last_name'] else "Nachname ✗"

        self.output_label.config(text=f"{first_name_feedback} {last_name_feedback}")
        if self.first_name_only.get(): # Checkbox "Vorname reicht aus" angehakt
            if results['first_name']:
                self.handle_correct_guess()
            else:
                self.handle_incorrect_guess()
        else: # Vor- UND Nachname erforderlich
            if results['first_name'] and results['last_name']:
                self.handle_correct_guess()
            else:
                self.handle_incorrect_guess()

    def handle_correct_guess(self):
        self.update_statistics_on_success()
        folder_path = os.path.join(Memory.IMAGES_FOLDER, self.current_folder)
        image_path = self.find_image(folder_path, "funny")
        self.guessed_folders.append(self.current_folder)
        self.display_image = self.resize_image(image_path)
        self.image_label.config(image=self.display_image)
        self.error_count = 0
        self.root.after(Memory.WAIT_TIME_BEFORE_NEXT, self.load_next_image) # Warte WAIT_TIME_BEFORE_NEXT und lade dann das nächste Bild

    def hint_first_name(self):
        last_name, first_name = self.current_folder.split('-')
        full_name = f"{first_name} {last_name}"
        hint = self.hint_giver.get_first_name_hint(first_name, full_name)
        self.output_label.config(text=f"Vorname Hinweis: {hint}")
        self.current_tip_count += 1
        self.update_round_label()
        self.statistics.hints_given += 1
        self.statistics.first_name_incorrect += 1
        self.handle_incorrect_guess()

    def hint_last_name(self):
        last_name, first_name = self.current_folder.split('-')
        full_name = f"{first_name} {last_name}"
        hint = self.hint_giver.get_last_name_hint(last_name, full_name)
        self.output_label.config(text=f"Nachname Hinweis: {hint}")
        self.current_tip_count += 1
        self.update_round_label()
        self.statistics.hints_given += 1
        self.statistics.last_name_incorrect += 1
        self.handle_incorrect_guess() 

    def solve_guess(self):
        last_name, first_name = self.current_folder.split('-')
        self.output_label.config(text=f"Name: {first_name} {last_name}")
        self.root.after(Memory.WAIT_TIME_BEFORE_NEXT, self.load_next_image)  # Warte WAIT_TIME_BEFORE_NEXT und lade dann das nächste Bild

    def handle_incorrect_guess(self):
        self.update_statistics_on_failure()
        self.error_count += 1
        if self.error_count >= Memory.MAX_ERRORS:
            self.show_person_name()
            self.error_count = 0
            self.root.after(500, self.load_next_image)
        else:
            folder_path = os.path.join(Memory.IMAGES_FOLDER, self.current_folder)
            image_path = self.find_image(folder_path, "normal")
            self.display_image = self.resize_image(image_path)
            self.image_label.config(image=self.display_image)

    def show_person_name(self):
        last_name, first_name = self.current_folder.split('-')
        self.output_label.config(text=f"Name: {first_name} {last_name}")

    def find_image(self, folder_path, keyword):
        for file in os.listdir(folder_path):
            if keyword in file and file.endswith(('.png', '.jpg', '.jpeg')):
                return os.path.join(folder_path, file)
        return None    
    
    def update_round_label(self):
        self.round_label.config(text=f"Runde {self.statistics.total_rounds}\n\n Tipp {self.current_tip_count} (von {Memory.MAX_ERRORS})")  # Aktualisiert das Runden-Label mit der aktuellen Runden- und Tipp-Anzahl

    def load_next_image(self):
        self.statistics.total_rounds += 1
        self.current_tip_count = 1  # Setzt die Anzahl der Tipps für die neue Person zurück
        self.update_round_label()  # Aktualisiert die Anzeige für die Runde und Tipp-Anzahl
        self.hint_giver.reset_hints()
        self.entry.delete(0, tk.END)
        self.output_label.config(text="Bitte Vor- und Nachnamen eingeben:")

        if self.statistics.total_rounds > 0:
            folders = [folder for folder in os.listdir(Memory.IMAGES_FOLDER) if folder not in self.guessed_folders]
            if not folders:
                self.output_label.config(text="Alle Personen wurden erraten!")
                return

        self.current_folder = random.choice(folders)
        folder_path = os.path.join(Memory.IMAGES_FOLDER, self.current_folder)
        image_path = self.find_image(folder_path, "normal")

        if image_path is not None:
                self.display_image = self.resize_image(image_path)
                self.image_label.config(image=self.display_image)
                self.image_label.pack()

    def on_close(self):
        if self.statistics.total_rounds > 0: # Aktualisiere die Statistik nur, wenn mindestens eine Runde gespielt wurde
            if self.current_tip_count > 1:
                self.statistics.total_incorrect += 1
        self.root.destroy()
        self.statistics.show_statistics()

    def run(self):
        self.root.mainloop()

    def resize_image(self, image_path):
        if image_path is None:
            return None
        image = Image.open(image_path)
        image.thumbnail((390, 390), Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def update_statistics_on_success(self):
        self.statistics.total_correct += 1
        if SimilarityCheck.check_similarity(self.entry.get().split()[0], self.current_folder.split('-')[1]): # Überprüfe: Falls keine Leereingabe vorliegt: Sind zwei Elemente vorhanden - Vor- und Nachname
            self.statistics.first_name_correct += 1
        if SimilarityCheck.check_similarity(self.entry.get().split()[-1], self.current_folder.split('-')[0]):
            self.statistics.last_name_correct += 1

    def update_statistics_on_failure(self):
        self.statistics.total_incorrect += 1
        guess_parts = self.entry.get().split()    

        if len(guess_parts) >= 2:
            if not SimilarityCheck.check_similarity(guess_parts[0], self.current_folder.split('-')[1]):
                self.statistics.first_name_incorrect += 1
            if not SimilarityCheck.check_similarity(guess_parts[-1], self.current_folder.split('-')[0]):
                self.statistics.last_name_incorrect += 1
        else:
            if len(guess_parts) == 1: # Wenn keine zwei Elemente: Überprüfe sowohl auf Vor- als auch auf Nachname
                self.statistics.first_name_incorrect += 1 # ÄNDERN
                self.statistics.last_name_incorrect += 1 # ÄNDERN
            else:
                # Wenn Leereingabe: Erhöhe "Inkorrekt" - Zähler für Vor- und Nachnamen
                self.statistics.first_name_incorrect += 1
                self.statistics.last_name_incorrect += 1
            
if __name__ == "__main__":
    game = Memory()
    game.run()

            
