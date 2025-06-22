import random
import sys
import os

if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

class SimpleTweetGenerator:
    def __init__(self):
        self.templates = {
            'announcement': [
                "🚀 Exciting news from {company}! {message}",
                "Big announcement: {company} is {message} 🎉",
                "Hey everyone! {company} has {message} ✨"
            ],
            'question': [
                "What do you think about {topic}? Let us know! 💬",
                "Quick question: How do you feel about {topic}? 🤔",
                "{company} wants to know: What's your take on {topic}? 🗣️"
            ],
            'general': [
                "Check out what {company} is up to! {message} 🌟",
                "{company} update: {message} 💯",
                "From the {company} team: {message} 🔥"
            ]
        }
    
    def generate_tweet(self, company, tweet_type="general", message="Something awesome!", topic="innovation"):
        template_list = self.templates.get(tweet_type, self.templates['general'])
        template = random.choice(template_list)
        
        tweet = template.format(
            company=company,
            message=message,
            topic=topic
        )
        
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        
        return tweet

# Test
# generator = SimpleTweetGenerator()
# print("Test 1:", generator.generate_tweet("Starbucks", "question", topic="coffee"))
# print("Test 2:", generator.generate_tweet("Apple", "announcement", "releasing iOS update"))
# print("Test 3:", generator.generate_tweet("Tesla", "general", "changing the world"))