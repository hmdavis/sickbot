import tweepy
import sys
import data

#ENTER LOGIN INFO 
CONSUMER_KEY= 
CONSUMER_SECRET= 
ACCESS_TOKEN= 
ACCESS_TOKEN_SECRET= 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
#GLOBAL VARIABLES NEEDED IN LISTENER 
limit = 0 
n = 0 
tweets = [] 

#LISTENER CLASS 
class TweetListener(tweepy.StreamListener): 
    def on_status(self, status):
        global limit 
        global n  
        global tweets
        try:    
        # print status.text
            if(n < limit): 
                t = status.text.replace('\n',' ')
                try:
                    print("Received Tweet: " + str(t))
                except UnicodeEncodeError:
                    return True 
                tweets.append(t)
                n+=1 
            else: 
                return False 
        except Exception, e: 
            print >> sys.stderr, 'Encountered Exception:', e

    def on_error(self,status): 
        print >> sys.stderr, 'Encountered error with status code:', status
        return True 

    def on_timeout(self): 
        print >> sys.stderr, 'Timeout...'
        return True

#METHOD TO BUILD THE LIST OF TWEETS 
# param: n is the number of tweets you want
# param: terms is the terms you want to filter the search by 
def getTweets(n, terms = data.searchterms): 
    global limit
    global tweets
    
    # Clear old tweets
    tweets = []
    
    limit = n
     
    search = terms
    if(terms == None):
        search =  ""
    
    stream = tweepy.streaming.Stream(auth, TweetListener(), timeout=60)
    
    print 'Filtering the public timeline for "%s"' % (' '.join(search),)
    stream.filter(follow=None, track = terms)
    
    return tweets