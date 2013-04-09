# This is a final project for CS 4701 by Alex Rablau and Harry Davis
# Using twitter API
import os
import tweetstreamer
import data
import re
from trainer import Trainer
from learner import Learner

# Trainer class to train the model
trainer = Trainer()
# Learner class to learn from new data
learner = Learner()

def main():
    
    # Welcome the user and ask them for what they want to do
    print("************************************")
    print("WELCOME TO THE TWITTER FLU DETECTOR!")
    print("************************************")
    
    # Read existing model into memory
    readExistingModel()   
    
    # Program main loop
    while(True):
        print("\nOptions:")
        print("1: Train Model\n2: Run Model\n3: Quit\n")            
        inputstring = raw_input("Enter option: ")
        if(inputstring == "1"):
            trainModel()
            saveEverythingToFile()
        elif(inputstring == "2"):
            runModel()
        elif(inputstring == "3"):
            print("Stay Healthy!")
            quit()
        else:
            print("\nThat is not an option!\n")
                    

# Read in existing data
def readExistingModel():
    if(os.path.exists("./probabilities.txt")):
        probsFile = open("./probabilities.txt","r")
        data.probOfFlu = float(probsFile.readline())
        probsFile.close()
        
        print("Trained model found!\n")
        
        readProbabilitiesFromFile()
        
    else:
        print("No trained model found!")
    pass

# Train the model
def trainModel():
    # Check if probabilities already exist and ask user if they want to use these probs
    if(len(data.probabilities) != 0):
        print("Saved model already exists.\nUse this model?\n")
       
        while(True):                                
            inputstring = raw_input("(y/n): ")
            if(inputstring == "y"):
                print("Model trained!")
                return
            elif(inputstring == "n"):
                data.probabilities.clear()
                break
            elif(inputstring == "q"):
                print("Good bye!")
                quit()
            ## TODO EXIT ##
            else:
                print("Please enter y, n, or q to quit")
                
    # Read tweets and categorization data from files    
    if(os.path.exists("./tweets.txt")):
        tweetsFile = open("./tweets.txt","r")
        data.tweetsStored = int(tweetsFile.readline())
        tweetsFile.close()
            
        print("Found tweets.txt with " + str(data.tweetsStored) + " tweets in it!")
            
        # Load tweets into memory
        readTweetsFromFile()
            
        # Check if training data already exists for these tweets
        if(os.path.exists("./trainingdata.txt")):
            trainingDataFile = open("./trainingdata.txt")
            data.tweetsCategorized = int(trainingDataFile.readline())
            trainingDataFile.close()
                
            print("Found trainingdata.txt with " + str(data.tweetsCategorized) + " categorizations in it!")
                
            if(data.tweetsStored < data.tweetsCategorized):
                # We have more categorized tweets than tweets themselves. Error
                print("Mismatch: more tweets are categorized than exist! Disregarding categorization data.")
                data.tweetsCategorized = 0
                    
            else:
                readCategorizationFromFile()
        else:
            print("No categorization data exists for these tweets!\n")
            
            
    # Ask the user how many tweets they would like in the training set        
    print("Please enter the number of tweets you would like in the training set")                     
    inputstring = raw_input(">> ")
    tweetsWanted = int(inputstring)

    # If we do not have enough tweets as the user requested
    if(data.tweetsStored < tweetsWanted):
        print(str(data.tweetsStored) + " tweets already stored.")
        print(str(tweetsWanted - data.tweetsStored) + " more tweets needed.")
                          
        print("Append more tweets or overwrite and collect new tweets?") 
                         
        while(True):                                
            inputstring = raw_input("(a/o): ")
            if(inputstring == "a"):
                data.tweets.append(tweetstreamer.getTweets(tweetsWanted - data.tweetsStored, data.searchterms))
                trainer.categorizeTweets()
                break
            elif(inputstring == "o"):
                data.tweetsStored = 0
                data.tweetsCategorized = 0
                data.tweets = tweetstreamer.getTweets(tweetsWanted - data.tweetsStored, data.searchterms)
                trainer.categorizeTweets()
                break
            elif(inputstring == "q"):
                print("Good bye!")
            ## TODO EXIT ##
            else:
                print("Please enter a to append, o to overwrite, or q to quit")
                    
    # We have more than enough tweets
    elif(data.tweetsStored >= tweetsWanted):
        print(str(data.tweetsStored) + " tweets already stored.")
                          
        print("Use these tweets or overwrite and collect new tweets?") 
                           
        while(True):                                
            inputstring = raw_input("(u/o): ")
            if(inputstring == "u"):
                readCategorizationFromFile()
                break
            elif(inputstring == "o"):
                data.tweetsStored = 0
                data.tweetsCategorized = 0
                data.tweets = tweetstreamer.getTweets(tweetsWanted - data.tweetsStored, data.searchterms)
                trainer.categorizeTweets()
                break
            elif(inputstring == "q"):
                print("Good bye!")
                quit()
            else:
                print("Please enter a to append, o to overwrite, or q to quit")      
           
    # Now we have the tweets and some categorization or not
    # Model is now trained
    # Model is stored in probabilities
    data.tweetsStored = len(data.tweets)
    trainer.calculateProbs()
    
# Run the model
def runModel():
    print("Model running mode!\n")
    
    print("Collecting 10 tweets to iterate through!")
    data.testTweets = tweetstreamer.getTweets(10)
    
    print("Use learning?")                
    goodinput = 0           
    while(not goodinput):                                
        inputstring = raw_input("(y/n): ")
        if(inputstring == "y"):
            useLearning = True
            goodinput = 1
        elif(inputstring == "n"):
            useLearning = False
            goodinput = 1
        else:
            print("Please enter y or n")
    
    # runModel main loop
    while(len(data.testTweets) != 0):
        print("\n1: Evaluate new tweet\n2: Exit running mode")             
        inputstring = raw_input("Enter option: ")
        if(inputstring == "1"):
            newTweet = data.testTweets.pop()
            wordsInTweet = re.findall(r'\w+', newTweet.lower()) 
            probTweetFlu = probOfFlu(wordsInTweet)
            isTweetFlu = probTweetFlu > data.THRESHOLD
            if(isTweetFlu):
                data.numFluTweets += 1
            try:
                print("\nNew tweet: " + str(newTweet))
                print("Probability the user has flu: " + str(probTweetFlu))
            except UnicodeEncodeError:
                print("Codec cannot encode characters in this tweet!")
            
            if(useLearning):
                learner.updateProbs(wordsInTweet, isTweetFlu)
        elif(inputstring == "2"):
            return
        else:
            print("\nThat is not an option!\n")
            
    print("All test tweets evaluated!!!")

# Calculate if this list of words indicates the flu
def probOfFlu(words):
    print("Enter prob of flu")
    probs = {}
    productOfProbs = 1
    productOfOneMinusProbs = 1
    
    # Calculate P(Flu|Word) for each word
    for w in words:        
        probFluGivenWord = fluGivenWord(w)
        probs[w] = probFluGivenWord
    
    # Calculate components of the final probability calculation
    for k in probs:
        productOfProbs *= probs[k]
        productOfOneMinusProbs *= (1 - probs[k])
        
    # Calculate probability
    probHasFlu = (productOfProbs / (productOfProbs + productOfOneMinusProbs))
    
    return probHasFlu

 
# Calculate P(Flu|Word)  
def fluGivenWord(word): 
    probOfHealth = 1 - data.probOfFlu 

    if word not in data.probabilities: 
        data.probabilities[word] = (0.4, 0.4)

    (probWordGivenFlu, probWordGivenHealth) = data.probabilities[word] 
       
    num = data.probOfFlu * probWordGivenFlu
    denom = probWordGivenFlu * data.probOfFlu + probWordGivenHealth * probOfHealth
    
    ans = num / denom
    if(ans == 0.0):
        ans = 0.01
    elif(ans == 1.0):
        ans = 0.99
        
    return ans

def readTweetsFromFile():
    tweetsFile = open("./tweets.txt", "r")
    data.tweetsStored = int(tweetsFile.readline())
         
    for line in tweetsFile:
        data.tweets.append(line)
        
    tweetsFile.close()
    
def readCategorizationFromFile():
    
    trainingDataFile = open("./trainingdata.txt", "r")
    
    data.tweetsCategorized = int(trainingDataFile.readline())
        
    for line in trainingDataFile:
        try:
            tweetnumber, isFlu = line.split()
        except ValueError:
            print("trainingdata.txt is not properly formatted!")
            return
            
        data.categorization[int(tweetnumber)] = int(isFlu)
        
    trainingDataFile.close()
    
def readProbabilitiesFromFile():
    
    probsFile = open("./probabilities.txt", "r")
    
    data.tweetsStored = float(probsFile.readline())
    data.probOfFlu = float(probsFile.readline())
    
    data.numFluTweets = data.tweetsStored * data.probOfFlu
    data.numHealthyTweets = data.tweetsStored * (1 - data.probOfFlu)
    
    for line in probsFile:
        try:
            word, probWordGivenFlu, probWordGivenHealthy = line.split()
        except ValueError:
            print("probabilities.txt is not properly formatted!")
            return
        
        data.probabilities[word.lower()] = float(probWordGivenFlu), float(probWordGivenHealthy)
        
    probsFile.close()
            
def saveEverythingToFile():
    saveTweetsToFile()
    saveCategorizationToFile()
    saveProbabilitiesToFile()
    
def saveTweetsToFile():
    
    tweetsFile = open("./tweets.txt", "w")
    
    tweetsFile.write(str(data.tweetsStored) + "\n")
        
    for tweet in data.tweets:
        tweetsFile.write(tweet + "\n")
        
    tweetsFile.close()
    
def saveCategorizationToFile():
    
    trainingDataFile = open("./trainingdata.txt", "w")
    
    trainingDataFile.write(str(data.tweetsCategorized) + "\n")
        
    for tweetNum, cat in data.categorization.iteritems():
        trainingDataFile.write(str(tweetNum) + " " + str(cat) + "\n")
        
    trainingDataFile.close()
    
def saveProbabilitiesToFile():
    
    probabilitiesFile = open("./probabilities.txt", "w")
    probabilitiesFile.write(str(data.tweetsStored) + "\n")
    probabilitiesFile.write(str(data.probOfFlu) + "\n")
        
    for word in data.words:
        probWordGivenFlu, probWordGivenHealthy = data.probabilities[word]
        probabilitiesFile.write(word + " " + str(probWordGivenFlu) + " " + str(probWordGivenHealthy) + "\n")
        
    probabilitiesFile.close()

# Start the program
main()

print("DONE!")

