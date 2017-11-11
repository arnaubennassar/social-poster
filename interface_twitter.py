import twitter

from env import twitter_consumer_key, twitter_consumer_secret, twitter_access_key, twitter_access_secret

api = twitter.Api(
	consumer_key=twitter_consumer_key, 
	consumer_secret=twitter_consumer_secret,
    access_token_key=twitter_access_key, 
    access_token_secret=twitter_access_secret,
#	input_encoding=encoding
)
def twitVideo (path, message):
	err = False
	try:
	    status = api.PostUpdate(message, media=path)
	except (UnicodeDecodeError, twitter.error.TwitterError) as e:
		err = True
		ret = dict(success=False, message=e)
	if err:
		return ret
	return dict(success=True, message="%s just posted: %s" % (status.user.name, status.text))



#print twitVideo('Hey, this is the twit message','/Users/arnaubennassarformenti/Downloads/Volley_Feroe_cut_min38.30.mp4')