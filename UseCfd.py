import nltk
import BuildCfd
import re,commands
from nltk.corpus import wordnet as wn
#from BuildCfd import frequency
cfd = BuildCfd.getCfd()


#Mapping from Nltk's Pos tags to Wordnet's Pos tag
morphy_tag = {'NN':wn.NOUN,'JJ':'a','VB':'v','RB':'r'}

def BuildAnswerDict(posDict):
    bestSentDict = {}
    for pos,word in posDict.iteritems():
        if word not in cfd[pos].keys():
            continue
        #Object with all sentences mapped by the word, and probability for each sentence for the word
        freqObj = cfd[pos][word]
        cfdDict = freqObj.getSentDict()
        sumFreq = freqObj.getSum()
        for sentence,freq in cfdDict.iteritems():
            if sentence not in bestSentDict.keys():
                bestSentDict[sentence] = float(freq/sumFreq)
            else:
                bestSentDict[sentence] = bestSentDict[sentence] + float(freq/sumFreq)
    return bestSentDict

def BuildBestAnswer(inpToken):
    ansDict = BuildAnswerDict(inpToken)
    maxFreq = 0
    bestAnswer = ""
    for sentence, freq in ansDict.iteritems():
        if freq>=maxFreq:
            maxFreq = freq
            bestAnswer = sentence
    return bestAnswer

            
if __name__ == '__main__':
    #bestAnswers = BuildBestAnswer()
    inp="pos"
    while not inp=="Bye":
        inp = raw_input('You>')
        inp = re.sub("[^A-Za-z]"," ",inp)
        inp = inp.lower()
        inpToken = nltk.word_tokenize(inp)
        posDict = BuildCfd.ProcessInp(inpToken)
        result = BuildBestAnswer(posDict)
        print 'Bot:'+result;
        print commands.getoutput("/usr/bin/espeak -v en+f4 -p 99 -s 160 \"" + result + "\"")