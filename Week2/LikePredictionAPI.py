from flask import Flask, request, jsonify
import joblib
import numpy as np
from textblob import TextBlob
import emoji
from datetime import datetime
import pandas as pd
app =Flask(__name__)
model = joblib.load('like_predictor.pkl')
scaler = joblib.load('scaler.pkl')
company_avg_likes_lookup = joblib.load('company_avg_likes.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    required_fields = ['id', 'date', 'content', 'username', 'media', 'inferred_company']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    content = data['content']
    date = data['date']
    media = data['media']
    inferred_company = data['inferred_company']
    word_count = len(content.split())
    char_count = len(content)
    has_media = 1 if media and media != '[]' else 0
    try:
        post_date = datetime.strptime(date, '%Y-%m-%d')
        hour = post_date.hour
    except ValueError as e:
        return jsonify({'error': f'Invalid date format: {str(e)}'}), 400
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
    return jsonify({'predicted_likes': int(prediction)})

if __name__ == "__main__":
    app.run(debug=True)
