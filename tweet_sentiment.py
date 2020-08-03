import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob
import twitter 

class TwitterClient(object): 
	def __init__(self): 
		consumer_key = 't1rCVWtOqZCwOX3y2yK03uKK4'
		consumer_secret = 'NAfExpSIAKTGmBPPMQPRWCITivK5WoDJWIUagbmexDedEInfCT'
		access_token = '831458946518913024-fczFWbJwBGMdaBaYx9zlHEenxcJPrre'
		access_token_secret = 'M4MTKVYTpAuFzo9ceIj2QtKbtt0CCfLoZXYmFpSUaVtR4'
		try: 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			self.auth.set_access_token(access_token, access_token_secret) 
			self.api = tweepy.API(self.auth)
			self.au = twitter.oauth.OAuth(access_token, access_token_secret,consumer_key, consumer_secret) 
		except: 
			print("Error: Authentication Failed")

	@staticmethod
	def num_format(num):
		if(num==None):
			pass
		elif num > 1000000:
			return(str(num/1000000)+'M')
		elif num > 1000:
			return(str(num/1000)+'K') 

	def trending_tweets(self):
		twitter_api = twitter.Twitter(auth=self.au)
		INDIA_WOE_ID = 23424848
		india_trends = twitter_api.trends.place(_id=INDIA_WOE_ID)
		print("\n[TOP 10] INDIA TRENDS: \n")
		num=0
		for trending in india_trends[0]['trends'][0:10]:
			num+=1
			print(str(num)+". "+trending['name'],'\n',TwitterClient.num_format(trending['tweet_volume']),'Tweets',end="\n\n") 
	
	def clean_tweet(self,tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet): 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count): 
		tweets = [] 

		try: 
			fetched_tweets = self.api.search(q = query, count = count,lang='en') 
			for tweet in fetched_tweets:
				if tweet.lang == "en":	
					parsed_tweet = {} 
					parsed_tweet['text'] = tweet.text 
					parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

					if tweet.retweet_count > 0: 
						if parsed_tweet not in tweets: 
							tweets.append(parsed_tweet) 
					else: 
						tweets.append(parsed_tweet) 
			return tweets 
		except tweepy.TweepError as e: 
			print("Error : " + str(e)) 

def main():
	api = TwitterClient() 
	api.trending_tweets()
	query = input("\nEnter tweet for sentiment analysis: ")
	tweets = api.get_tweets(query , count = 100) 
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
	print("Positive tweets percentage: {:.2f} %".format(100*len(ptweets)/len(tweets))) 
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
	print("Negative tweets percentage: {:.2f} %".format(100*len(ntweets)/len(tweets))) 
	print("Neutral tweets percentage: {:.2f} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 

	neutraltweets=[tweet for tweet in tweets if tweet['sentiment']=='neutral']
	print("\n\nPOSITIVE TWEETS:\n") 
	for tweet in ptweets[:10]: 
		print(tweet['text']) 

	print("\n\nNEGATIVE TWEETS:\n") 
	for tweet in ntweets[:10]: 
		print(tweet['text']) 

	print("\n\nNEUTRAL TWEETS:\n") 
	for tweet in neutraltweets[:10]: 
		print(tweet['text']) 
	print()

if __name__ == "__main__": 
	main() 

