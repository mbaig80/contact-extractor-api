from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)  # Enables access from your offline HTML

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        res = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text()

        # Extract phone numbers
        phones = re.findall(r'\+?\d[\d\s\-\(\)]{7,}\d', text)
        phones = list(set(phones))  # Remove duplicates

        # Extract emails (optional)
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        emails = list(set(emails))

        return jsonify({'url': url, 'phones': phones, 'emails': emails})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
