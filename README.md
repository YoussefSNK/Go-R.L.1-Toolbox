# YouTube Video Downloader

Une application web pour télécharger des vidéos YouTube facilement.

## Prérequis

- Python 3.7 ou supérieur
- Navigateur web moderne

## Installation

1. Clonez ce dépôt:
   ```
   git clone <url-du-repo>
   cd <nom-du-repo>
   ```

2. Installez les dépendances:
   ```
   pip install -r requirements.txt
   ```

## Utilisation

1. Lancez l'application:
   ```
   python dl_youtube.py
   ```

2. Ouvrez votre navigateur et accédez à:
   ```
   http://127.0.0.1:5000/
   ```

3. Entrez l'URL d'une vidéo YouTube dans le champ de texte et cliquez sur "Télécharger".

4. Les vidéos téléchargées seront sauvegardées dans le dossier "Video".

## Fonctionnalités

- Interface web simple et intuitive
- Historique des téléchargements
- Affichage des statuts de téléchargement
- Téléchargement rapide grâce à yt-dlp