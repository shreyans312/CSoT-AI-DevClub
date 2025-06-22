import requests

# Test prediction API (from Week 2)
prediction_response = requests.post('http://localhost:5000/predict', json={
    "id": 1,
    "date": "2019-06-11",
    "content": "This is the sample text for my like prediction api",
    "username": "ShreyansJain",
    "media": "[Photo(previewUrl='https://pbs.twimg.com/media/ELsYh1LXsAAzPb_?format=jpg&name=small', fullUrl='https://pbs.twimg.com/media/ELsYh1LXsAAzPb_?format=jpg&name=large')]",
    "inferred_company": "cnn"
})

# Test generation API (from Week 3)  
generation_response = requests.post('http://localhost:5001/generate', json={
    'company': 'Tesla',
    'tweet_type': 'announcement',
    'message': "We're unveiling something big",
})

print("Predicted Likes:", prediction_response.json())
print("Generated Tweet:", generation_response.json())