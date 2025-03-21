import os
import subprocess
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

# Create templates directory if it doesn't exist
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        
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
            'status': 'pending',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        session.modified = True
        
        # Process download
        try:
            print(f"Téléchargement de la vidéo depuis : {url}")
            subprocess.run(
                ["yt-dlp", url, "-o", os.path.join(output_dir, "%(title)s.%(ext)s")],
                check=True
            )
            session['downloads'][download_id]['status'] = 'success'
            flash('Téléchargement terminé avec succès!', 'success')
        except subprocess.CalledProcessError as e:
            session['downloads'][download_id]['status'] = 'error'
            session['downloads'][download_id]['error'] = str(e)
            flash(f'Erreur lors du téléchargement: {e}', 'error')
        except Exception as e:
            session['downloads'][download_id]['status'] = 'error'
            session['downloads'][download_id]['error'] = str(e)
            flash(f'Erreur inattendue: {e}', 'error')
        
        session.modified = True
        return redirect(url_for('index'))
    
    # Get downloads from session
    downloads = session.get('downloads', {})
    return render_template('index.html', downloads=downloads)

@app.route('/clear-history', methods=['POST'])
def clear_history():
    if 'downloads' in session:
        session.pop('downloads')
    flash('Historique effacé', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create the template file if it doesn't exist
    template_path = os.path.join(templates_dir, "index.html")
    if not os.path.exists(template_path):
        with open(template_path, "w", encoding="utf-8") as f:
            f.write('''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Video Downloader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #cc0000;
            text-align: center;
        }
        form {
            display: flex;
            margin-bottom: 20px;
        }
        input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px 0 0 4px;
        }
        button {
            padding: 10px 20px;
            background-color: #cc0000;
            color: white;
            border: none;
            border-radius: 0 4px 4px 0;
            cursor: pointer;
        }
        button:hover {
            background-color: #990000;
        }
        .history {
            margin-top: 30px;
        }
        .download-item {
            padding: 10px;
            margin-bottom: 10px;
            border-left: 4px solid #ddd;
            background-color: #f9f9f9;
        }
        .download-item.success {
            border-left-color: #28a745;
        }
        .download-item.error {
            border-left-color: #dc3545;
        }
        .download-item.pending {
            border-left-color: #ffc107;
        }
        .flash-messages {
            margin-bottom: 20px;
        }
        .flash {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 4px;
        }
        .flash.success {
            background-color: #d4edda;
            color: #155724;
        }
        .flash.error {
            background-color: #f8d7da;
            color: #721c24;
        }
        .flash.info {
            background-color: #d1ecf1;
            color: #0c5460;
        }
        .clear-history {
            text-align: right;
        }
        .clear-button {
            background-color: #6c757d;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>YouTube Video Downloader</h1>
        
        {% if get_flashed_messages() %}
        <div class="flash-messages">
            {% for category, message in get_flashed_messages(with_categories=true) %}
                <div class="flash {{ category }}">{{ message }}</div>
            {% endfor %}
        </div>
        {% endif %}
        
        <form method="post">
            <input type="text" name="url" placeholder="Entrez l'URL de la vidéo YouTube" required>
            <button type="submit">Télécharger</button>
        </form>
        
        {% if downloads %}
        <div class="history">
            <h2>Historique des téléchargements</h2>
            
            <div class="clear-history">
                <form method="post" action="{{ url_for('clear_history') }}">
                    <button type="submit" class="clear-button">Effacer l'historique</button>
                </form>
            </div>
            
            {% for id, download in downloads.items() %}
            <div class="download-item {{ download.status }}">
                <p><strong>URL:</strong> {{ download.url }}</p>
                <p><strong>Statut:</strong> 
                    {% if download.status == 'success' %}
                        Téléchargé avec succès
                    {% elif download.status == 'error' %}
                        Échec du téléchargement
                        {% if download.error %}
                        <br><small>{{ download.error }}</small>
                        {% endif %}
                    {% elif download.status == 'pending' %}
                        En attente
                    {% endif %}
                </p>
                <p><small>{{ download.time }}</small></p>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
</body>
</html>''')

    app.run(debug=True)