# -*- coding: utf-8 -*-
import MeCab
import unicodedata
import re
from collections import Counter


class MecabParser:

    def __init__(self):
        self.tagger = MeCab.Tagger("-Ochasen")

    def extract_place(self, text):
        #def extract_place(self, node):
        #places = []
        #while node:
        #    if node.feature.split(',')[2] == '地域' and node.feature.split(',')[1] == '固有名詞':
        #        places.append(node.surface)
        #    node = node.next
        #return places
        places = []
        subParsed = self.tagger.parseNBest(3, text)
        for parts in subParsed.split("EOS\n"):
            dividedPlaces = []
            for res in parts.split("\n"):
                splitRes = res.split("\t")
                if len(splitRes) > 1 and re.search("地域", splitRes[3]) and self.check_unnecessary(splitRes[0]) != None:
                    dividedPlaces.append(splitRes[0])
                    #places.append(splitRes[0])
            places = places + list((Counter(dividedPlaces) - Counter(places)).elements())
        return places



    def noun_place(self, text, nbest = None):
        text = text.encode('utf-8')
        normalized = self.normalize(text)
        node = self.tagger.parseToNode(normalized)
        #return self.extract_noun(node, omit=True, nbest=nbest), self.extract_place(node)
        return self.extract_noun(node, omit=True, nbest=nbest), self.extract_place(normalized)


    def parse(self, text, omit=True, nbest=None):
        node = self.tagger.parseToNode(self.normalize(text))
        return self.extract_noun(node, omit=omit, nbest=nbest)


    def extract_noun(self, node, omit = True, nbest = None):
        nouns = []
        while node:
            if self.check_morpheme(node):
                noun = node.surface
                if omit:
                    #if len(noun) > 1 and self.check_unnecessary(noun) != None:
                    if (len(noun) > 1 or re.match("固有名詞", node.feature(node).split(",")[1])) and self.check_unnecessary(noun) != None:
                        nouns.append(noun)
                else:
                    nouns.append(noun)
            node = node.next
        if nbest != None:
            subNouns = []
            lnouns = [x for x in noun if len(x) > 1]
            for noun in lnouns:
                subParsed = self.tagger.parseNBest(nbest, noun)
                subNounNonUniq = []
                for parts in subParsed.split("EOS\n"):
                    for res in parts.split("\n"):
                        splitRes = res.split("\t")
                        if len(splitRes) > 4 and re.match("固有名詞", splitRes[3]) and self.check_unnecessary(splitRes[0]) != None:
                            subNounNonUniq.append(splitRes[0])
                subNouns = subNouns + list(set(subNounNonUniq) - set([noun]))
            return nouns + subNouns
        return nouns

    def normalize(self, text):
        normalized = unicodedata.normalize('NFKC', text.decode('utf-8'))
        normalized = normalized.lower()
        return normalized.encode('utf-8')
        
        
    def check_morpheme(self, node, flag=True):
    	test = False
    	if node.feature.split(",")[0] == '名詞':
    		test = True
    	if flag == True:
    		morphemeType = node.feature.split(',')[1]
    		if morphemeType in ['形容動詞語幹', '副詞可能', '接尾']:
    			return False
    	return test


    def check_unnecessary(self, noun):
        #string = noun.decode('utf-8')
        string = unicode(noun, 'utf-8', errors='ignore')
        kanji = re.search(u'[一-龠]', string)
        hiragana = re.search(u'[ぁ-ん]', string)
        katakana = re.search(u'[ァ-ヴ]', string)
        alphabet = re.search(u'[a-z]', string)
        
        #if len(string) == 1:
        #    return None
        #elif kanji == None and hiragana == None and katakana == None and alphabet == None:
        if kanji == None and hiragana == None and katakana == None and alphabet == None:
            return None
        elif kanji == None and hiragana != None and katakana == None and alphabet == None and len(string) < 3:
            return None
        elif kanji == None and len(string)  == 1:
            return None
        if re.search(u'^年度$', string):
            return None
        #if re.search(u'^([a-z]|[ぁ-ん]|[ァ-ヴ]|[一-龠]){4,}$', string):
        #if re.search(u'^([a-z]|[ぁ-ん]|[ァ-ヴ]|[一-龠]){2,}$', string) == None:
        #    return None
        return noun

