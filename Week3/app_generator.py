from flask import Flask, request, jsonify
from tweet_generator import SimpleTweetGenerator
import os
import sys

app = Flask(__name__)
generator = SimpleTweetGenerator()

if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        company = data.get('company', 'Our Company')
        tweet_type = data.get('tweet_type', 'general')
        message = data.get('message', 'Something awesome!')
        topic = data.get('topic', 'innovation')
        generated_tweet = generator.generate_tweet(company, tweet_type, message, topic)
        
        return jsonify({
            'generated_tweet': generated_tweet,
            'success': True,
            'company': company,
            'type': tweet_type
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Tweet Generator API is running!'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)