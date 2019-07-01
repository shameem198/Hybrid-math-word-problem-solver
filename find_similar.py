from collections import *
from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec,KeyedVectors
from gensim.test.utils import datapath
from nltk.corpus import wordnet

class find_similar:
    def __init__(self):
        return

    def most_similar(self,word,seedverbs,wvec):
        if word in seedverbs:
            return word
        synverb =[]
        antoverb = []
        category = 'v'
        synsetsForWord = wordnet.synsets(word, pos=category)
#        print(synsetsForWord)
        syall = wordnet.synsets(word)
        for syn in synsetsForWord:
            for l in syn.lemmas():
                synverb.append(l.name())
                if l.antonyms():
                    antoverb.append(l.antonyms()[0].name())
        msimilar = wvec.most_similar(word)
        #print(msimilar)
        for i in msimilar:
            if i[0] not in antoverb and i[0] in synverb and i[0] in seedverbs:
                return i[0]
            if (i[0] in synverb and i[0] in seedverbs):
                return i[0] 
        else:
            for i in synverb:
                if i in seedverbs:
                    return i
            for i in msimilar:
                if i[0] not in antoverb and i[0] in seedverbs:
                    return i[0]
            maxv = -1
            maxword = ""

            for i in seedverbs:
                if wvec.similarity(word,i) > maxv and i not in antoverb:
                    maxv= wvec.similarity(word,i)
                    maxword  = i
            return maxword
            maxv = -1
            maxword = ""

            for i in seedverbs:
                if wvec.similarity(word,i) > maxv and i not in antoverb:
                    maxv= wvec.similarity(word,i)
                    maxword  = i
            return maxword

