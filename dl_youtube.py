import subprocess

urls = "urls.txt"

try:
    with open(urls, "r") as f:
        urls = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"Erreur : Le fichier '{urls}' est introuvable.")
    exit(1)

resultats = []

for url in urls:
    try:
        print(f"Téléchargement de la vidéo depuis : {url}")
        subprocess.run(["yt-dlp", url, "-o", "%(title)s.%(ext)s"], check=True)
        resultats.append((url, "Succès"))
        print("Téléchargement terminé !")
    except subprocess.CalledProcessError as e:
        resultats.append((url, "Échec"))
        print(f"Erreur lors du téléchargement de {url} : {e}")
    except Exception as e:
        resultats.append((url, "Échec"))
        print(f"Erreur inattendue pour {url} : {e}")

print("\nRésumé des téléchargements :")
for url, statut in resultats:
    print(f"- {url} : {statut}")