import os
import subprocess
import sys
import shutil
from flask import Flask, render_template, request, redirect, url_for, flash, session
import uuid
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages

# Create output directory
output_dir = "Video"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Check if FFmpeg is available
def check_ffmpeg():
    """Check if FFmpeg is available in the system path or in the local directory."""
    # Check in system path
    ffmpeg_in_path = shutil.which('ffmpeg')
    if ffmpeg_in_path:
        return ffmpeg_in_path
    
    # Check in local directory
    local_ffmpeg = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg', 'bin', 'ffmpeg.exe')
    if os.path.exists(local_ffmpeg):
        return local_ffmpeg
    
    return None

ffmpeg_path = check_ffmpeg()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        format_type = request.form.get('format', 'video')  # Default to video if not specified
        
        if not url:
            flash('Veuillez entrer une URL valide', 'error')
            return redirect(url_for('index'))
        
        # Create a unique download ID
        download_id = str(uuid.uuid4())
        
        # Store download info in session
        if 'downloads' not in session:
            session['downloads'] = {}
            
        session['downloads'][download_id] = {
            'url': url,
            'format': format_type,
            'status': 'pending',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        session.modified = True
        
        # Process download
        try:
            print(f"Téléchargement de {format_type} depuis : {url}")
            
            # Base command
            command = ["yt-dlp", url, "-o", os.path.join(output_dir, "%(title)s.%(ext)s")]
            
            # Add specific arguments for mp3 format
            if format_type == 'mp3':
                if not ffmpeg_path and format_type == 'mp3':
                    session['downloads'][download_id]['status'] = 'error'
                    session['downloads'][download_id]['error'] = "FFmpeg non trouvé. Nécessaire pour la conversion en MP3."
                    flash("FFmpeg non trouvé. Nécessaire pour la conversion en MP3. Veuillez installer FFmpeg ou sélectionner le format vidéo.", 'error')
                    session.modified = True
                    return redirect(url_for('index'))
                
                command.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])
                
                # Add FFmpeg location if available
                if ffmpeg_path:
                    command.extend(["--ffmpeg-location", os.path.dirname(ffmpeg_path)])
            
            subprocess.run(command, check=True)
            
            session['downloads'][download_id]['status'] = 'success'
            flash(f'Téléchargement terminé avec succès! (Format: {format_type})', 'success')
        except subprocess.CalledProcessError as e:
            session['downloads'][download_id]['status'] = 'error'
            session['downloads'][download_id]['error'] = str(e)
            
            if 'ffprobe and ffmpeg not found' in str(e) and format_type == 'mp3':
                flash(f'Erreur : FFmpeg non trouvé. Nécessaire pour la conversion en MP3. Veuillez installer FFmpeg ou sélectionner le format vidéo.', 'error')
            else:
                flash(f'Erreur lors du téléchargement: {e}', 'error')
        except Exception as e:
            session['downloads'][download_id]['status'] = 'error'
            session['downloads'][download_id]['error'] = str(e)
            flash(f'Erreur inattendue: {e}', 'error')
        
        session.modified = True
        return redirect(url_for('index'))
    
    # Get downloads from session
    downloads = session.get('downloads', {})
    
    # Check FFmpeg status for template
    ffmpeg_status = {
        'available': ffmpeg_path is not None,
        'path': ffmpeg_path or 'Non trouvé'
    }
    
    return render_template('index.html', downloads=downloads, ffmpeg_status=ffmpeg_status)

@app.route('/clear-history', methods=['POST'])
def clear_history():
    if 'downloads' in session:
        session.pop('downloads')
    flash('Historique effacé', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Print FFmpeg status on startup
    if ffmpeg_path:
        print(f"FFmpeg trouvé: {ffmpeg_path}")
    else:
        print("ATTENTION: FFmpeg n'a pas été trouvé. Le téléchargement en format MP3 ne fonctionnera pas.")
        print("Veuillez installer FFmpeg et l'ajouter à votre PATH, ou le placer dans un dossier 'ffmpeg/bin' à côté de ce script.")
    
    app.run(debug=True)