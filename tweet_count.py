
import re 

#best regex for our purposes 
WORD_RE = re.compile(r"[\w']+")


def zip(occurances): 
  fst = 0
  snd = 0
  for o in occurances:
    if o == 1: fst += 1
    elif o == 0: snd += 1 
  zipped = (fst,snd)    #<number of flu tweets, number of not flu>  
  return zipped 

class TweetCounter(MRJob):

    def mapper(self, key, line):
        l= []
        #edit to match formatting 

        tag = int(line.split("***")[0]) #1 for flu, 0 otherwise
        new_line = line.split("***")[1] #tweet content 
        for word in WORD_RE.findall(new_line):  #break up tweet based on regex 
          if word not in l:       #ignore duplicates of words 
            l.append(word)
        for v in l:               #intermediate pair = <word,flu/not flu> 
          yield v, tag

    def reducer(self, word, occurrences):
        yield word, zip(occurrences)  #produce final tuple for each word 

if __name__ == '__main__':
    TweetCounter.run()