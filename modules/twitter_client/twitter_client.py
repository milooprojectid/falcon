import tweepy
import requests
import time

from modules.twitter_client.dict import trigger_words


class TwitterClient:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, db):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.auth = self.authentication()
        self.api = tweepy.API(self.auth)
        self.me = self.api.me()
        self.list_trigger_words = trigger_words
        self.db = db

    def authentication(self):
        self.auth = tweepy.OAuthHandler(
            self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        return self.auth

    def get_mention(self, since_id):
        new_since_id = since_id

        list_mentions = []

        for tweet in tweepy.Cursor(self.api.mentions_timeline, since_id=since_id).items():
            new_since_id = max(tweet.id, new_since_id)

            for trigger_word in self.list_trigger_words:
                if trigger_word in tweet.text:
                    list_mentions.append(tweet)

        self.process_tweet(list_mentions)

        return new_since_id

    def get_summary(self, text):
        url = "http://0.0.0.0:5001/summarize"
        data = {'text': text}
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            data = response.json()
            summary = data['data']['summary']
            return summary
        else:
            data = response.json()
            return data['message']

    def process_tweet(self, list_tweet):
        for tweet in reversed(list_tweet):
            urls = tweet.entities['urls']
            url = urls[-1]['expanded_url']

            summary = self.get_summary(url)
            status = f"Summary: {summary}\n {url}"

            try:
                self.api.update_status(
                    status=status,
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True)
                data = {'user_id': tweet.user.id, 'url_links': url,
                        'command': 'summarization', 'latest_mention_id': tweet.id}
                self.db.insert_object(data)

            except tweepy.TweepError as e:
                data = {'user_id': tweet.user.id, 'url_links': url,
                        'command': 'summarization', 'latest_mention_id': tweet.id}
                self.db.insert_object(data)
                print(e)

            print(f"Tweeting:\n{status}")
            time.sleep(60)
