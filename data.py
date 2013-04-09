
# Threshold probability to check if a tweet indicates the Flu
THRESHOLD = 0.85
# Terms that we want in the tweets we receive from twitter
searchterms = ["flu", "influenza", "sneeze", "ache", "cough", "fever"]
# Size of the training set
trainingSetSize = 0
# Number of tweets stored
tweetsStored = 0
# Actually tweets as list of strings
tweets = list()
# Number of tweets categorized
tweetsCategorized = 0
# Number of Flu Tweets
numFluTweets = 0
# Number of Healthy Tweets
numHealthyTweets = 0
# Probability of Flu tweet
probOfFlu = 0
# Categorization data
categorization = {}
# List of all words that appear in tweets
words = list()
# Dictionary from word to tuple of P(W|F) and P(W|H)
probabilities = {}

# Tweets to use for testing
testTweets = list()
