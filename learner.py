
import data

class Learner(): 
    def __init__(self): 
        pass

    def updateProbs(self, words ,is_flu): 
        if is_flu:
            for word in data.probabilities: 
                fluTweetsWithWord = data.probabilities[word][0] * (data.numFluTweets - 1) 
                if not word in words: 
                    data.probabilities[word] = ((fluTweetsWithWord / data.numFluTweets), data.probabilities[word][1]) 
                else: 
                    data.probabilities[word] = (((fluTweetsWithWord+1) / data.numFluTweets), data.probabilities[word][1]) 

        else: 
            for word in data.probabilities: 
                healthyTweetsWithWord = data.probabilities[word][1] * (data.numHealthyTweets - 1)
                if not word in words: 
                    data.probabilities[word] = (data.probabilities[word][0], (healthyTweetsWithWord / data.numHealthyTweets))
                else: 
                    data.probabilities[word] = (data.probabilities[word][0], ((healthyTweetsWithWord+1)/ data.numHealthyTweets))