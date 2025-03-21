# YouTube Video Downloader

Une application web pour télécharger des vidéos YouTube facilement.

## Prérequis

- Python 3.7 ou supérieur
- Navigateur web moderne
- FFmpeg (requis pour le téléchargement en format MP3)

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

3. Installez FFmpeg (nécessaire pour la conversion en MP3):
   - Windows:
     1. Téléchargez FFmpeg depuis [le site officiel](https://ffmpeg.org/download.html) ou [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (version "essentials")
     2. Extrayez l'archive dans un dossier de votre choix
     3. Soit:
        - Ajoutez le dossier bin de FFmpeg à votre PATH système
        - Ou créez un dossier `ffmpeg/bin` à la racine de ce projet et copiez-y les fichiers ffmpeg.exe, ffprobe.exe et ffplay.exe
   
   - macOS:
     ```
     brew install ffmpeg
     ```

   - Linux:
     ```
     sudo apt-get install ffmpeg
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

3. Sélectionnez le format souhaité (vidéo ou MP3 audio uniquement)

4. Entrez l'URL d'une vidéo YouTube dans le champ de texte et cliquez sur "Télécharger".

5. Les fichiers téléchargés seront sauvegardés dans le dossier "Video".

## Fonctionnalités

- Interface web simple et intuitive
- Choix du format: vidéo ou MP3 (audio uniquement) en haute qualité
- Historique des téléchargements
- Affichage des statuts de téléchargement
- Téléchargement rapide grâce à yt-dlp

## Résolution des problèmes

### Erreur "FFmpeg not found"
Si vous rencontrez cette erreur lors de la conversion en MP3, c'est que FFmpeg n'est pas correctement installé ou n'est pas trouvé dans le PATH. Suivez les instructions d'installation de FFmpeg indiquées ci-dessus.

### Option MP3 désactivée
L'option MP3 sera automatiquement désactivée si FFmpeg n'est pas trouvé sur votre système. Une fois FFmpeg correctement installé, redémarrez l'application pour activer cette option.