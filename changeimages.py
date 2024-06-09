from PIL import Image
import os

# Verzeichnis, in dem sich die Bilder befinden
input_directory = r"C:\Users\Michael Schmidt\OneDrive - SeitWerk GmbH\Dokumente\Python Scripts\Memory\MABilder"

# Verzeichnis, in dem die GIFs gespeichert werden sollen
output_directory = r"C:\Users\Michael Schmidt\OneDrive - SeitWerk GmbH\Dokumente\Python Scripts\Memory\ConvertedGIFs"

# Erstellen Sie das Ausgabeverzeichnis, wenn es nicht existiert
os.makedirs(output_directory, exist_ok=True)

# Funktion zur Umwandlung von Bildern in GIFs
def convert_to_gif(input_path, output_path):
    img = Image.open(input_path)
    img.save(output_path, "GIF")

# Durchsuchen Sie das Eingabeverzeichnis rekursiv
for root, dirs, files in os.walk(input_directory):
    for filename in files:
        if filename.endswith(".jpg"):
            input_path = os.path.join(root, filename)
            relative_path = os.path.relpath(input_path, input_directory)
            output_path = os.path.join(output_directory, os.path.splitext(relative_path)[0] + ".gif")

            # Erstellen Sie das Ausgabeverzeichnis für das GIF
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Konvertieren Sie das JPG-Bild in ein GIF
            convert_to_gif(input_path, output_path)

print("Alle Bilder wurden erfolgreich in GIFs umgewandelt.")
