from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from datetime import datetime
from flask import Flask, request, jsonify
import pandas as pd
from textblob import TextBlob
import joblib
import emoji
import numpy as np

model = joblib.load(r'like_predictor.pkl')
scaler = joblib.load(r'scaler.pkl')
company_avg_likes_lookup = joblib.load(r'company_avg_likes.pkl')

class AITweetGenerator:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def generate_ai_tweet(self, prompt, max_length=60):
        inputs = self.tokenizer.encode(prompt, return_tensors='pt')
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                temperature=0.8,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        tweet = generated_text[len(prompt):].strip()
        return tweet[:280]

app = Flask(__name__)

@app.route('/generate_ai', methods=['POST'])
def generate_ai():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error':'No input data provided'}), 400
        
        company = data.get('company', 'Our Company')
        tweet_type = data.get('tweet_type', 'general')
        message = data.get('message', 'Something awesome!')

        prompt = f"{company} {tweet_type} tweet: {message}"
        generator = AITweetGenerator()
        tweet_ai = generator.generate_ai_tweet(prompt)
        return jsonify({
            'generated_tweet': tweet_ai,
            'success': True,
            'company': company,
            'type': tweet_type
                        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False,
        }), 500

@app.route('/generate_and_predict', methods=['POST'])
def generate_and_predict():
    data = request.get_json()
    if not data:
            return jsonify({'error':'No input data provided'}), 400
        
    company = data.get('company', 'Our Company')
    tweet_type = data.get('tweet_type', 'general')
    message = data.get('message', 'Something awesome!')
    prompt = f"{company} {tweet_type} tweet: {message}"
    generator = AITweetGenerator()
    generated_tweet = generator.generate_ai_tweet(prompt)
    
    content = generated_tweet
    date = datetime.now()
    media = tweet_type
    inferred_company = company
    word_count = len(content.split())
    char_count = len(content)
    has_media = 1 if media and media != '[]' else 0
    hour = date.hour

    polarity = TextBlob(content).sentiment.polarity
    sentiment = TextBlob(content).sentiment.polarity

    emoji_count = len([char for char in content if char in emoji.EMOJI_DATA])
    has_hashtag = 1 if '#' in content else 0
    has_url = 1 if 'http' in content else 0
    company_avg_likes = company_avg_likes_lookup.get(inferred_company, 500)
    features = np.array([
        word_count,
        char_count,
        has_media,
        hour,
        sentiment,
        emoji_count,
        has_hashtag,
        has_url,
        company_avg_likes
    ]).reshape(1, -1)
    feature_names = ['word_count', 'char_count', 'has_media', 'hour', 'sentiment', 'emoji_count', 'has_hashtag', 'has_url', 'company_avg_likes']
    features_df = pd.DataFrame(features, columns=feature_names)
    features_scaled = scaler.transform(features_df)
    log_prediction = model.predict(features_scaled)
    prediction = int(np.expm1(log_prediction[0]))
    
    return jsonify({
        'generated_tweet': generated_tweet,
        'predicted_likes': int(prediction),
        'success': True
    })
  
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Tweet Generator API is running!'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
