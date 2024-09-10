from flask import Flask, request, jsonify
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Initialiser Flask
app = Flask(__name__)

# Configurer l'API YouTube Data V3
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'No query parameter provided'}), 400

    try:
        # Effectuer la recherche sur YouTube
        request = youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            order='relevance',
            maxResults=5
        )
        response = request.execute()

        # Extraire les informations des résultats
        results = []
        for item in response.get('items', []):
            results.append({
                'title': item['snippet']['title'],
                'videoId': item['id']['videoId'],
                'thumbnail': item['snippet']['thumbnails']['default']['url']
            })

        return jsonify({'results': results})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
