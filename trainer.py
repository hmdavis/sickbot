import os
import re
import operator
import data

            
# Map flu tweet to if it contains word [1 or 0] / number of flu tweets
# Reduce by adding
# This is P(W|F)
# Do map reduce again for healthy tweets to get P(W|H)
# P(F) and P(H) from total tweets
class Trainer():
    # Categorize tweets as flu or healthy from the tweets that exists in tweets.txt
    def categorizeTweets(self):
        print("\n********************\nEntering categorization mode\n********************\n")
        print("You will be prompted with tweets and asked to enter y if it is a flu tweet or n if it is not\n")
        print("Enter q to quit and store the latest categorization at any time!\n")
        
        # Loop from the last tweet categorized to the end
        for i in range(data.tweetsCategorized, len(data.tweets)):
            try:
                print("\n" + data.tweets[i])
            except UnicodeEncodeError:
                continue
            
            goodinput = 0           
            while(not goodinput):                 
                inputstring = raw_input("Does this user have the Flu? (y/n/q): ")
                if(inputstring == "y"):
                    data.categorization[i] = 1
                    goodinput = 1
                elif(inputstring == "n"):
                    data.categorization[i] = 0
                    goodinput = 1
                elif(inputstring == "q"):
                    print("Categorization saved to file!")
                    return
                else:
                    print("Please enter y to for Flu, n for not Flu, or q to save and quit")
                    
        data.tweetsCategorized = len(data.tweets)
        print("All tweets have been categorized!!\n")
    
    def calculateProbs(self):
        
        # Start with P(F) and P(H)
        fluTweets = list()
        healthTweets = list()
        
        # Split tweets into two lists. Flu and not Flu
        data.numFluTweets = 0
        for tweetNum, cat in data.categorization.iteritems():
            data.numFluTweets += cat
            if(cat == 0):
                healthTweets.append(data.tweets[tweetNum])
            else:
                fluTweets.append(data.tweets[tweetNum])
        
        data.numHealthyTweets = data.tweetsStored - data.numFluTweets
        
        data.probOfFlu = float(data.numFluTweets) / float(data.tweetsStored)
        
        print(data.probOfFlu)
        
        # Create a list of all words that occur in the training data
        for tweet in data.tweets:
            words = re.findall(r'\w+', tweet)
            
            for word in words:
                if(not word in data.words):
                    data.words.append(word)
                    
        
        # For each word:
        for word in data.words:
            # Get prob word given flu
            isWordInFluTweets = map(lambda x: operator.contains(x, word)/float(data.numFluTweets), fluTweets)
            probWordGivenFlu = reduce(operator.add, isWordInFluTweets)
            
            # Get prob word given healthy
            isWordInHealthTweets = map(lambda x: operator.contains(x, word)/float(data.numHealthyTweets), healthTweets)
            probWordGivenHealth = reduce(operator.add, isWordInHealthTweets)
            
            # Updata data in data
            data.probabilities[word] = probWordGivenFlu, probWordGivenHealth
            
        
        print("Probabilities calculated!!!")  

    
    
    
    
    