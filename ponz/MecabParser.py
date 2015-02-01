# -*- coding: utf-8 -*-
import MeCab
import unicodedata
import re

class MecabParser:

    def __init__(self):
        self.tagger = MeCab.Tagger("-Ochasen")

    def extract_place(self, node):
        places = []
        while node:
            if node.feature.split(',')[2] == '地域' and node.feature.split(',')[1] == '固有名詞':
                places.append(node.surface)
            node = node.next
        return places

    def extract_noun(self, node, omit=True):
        nouns = []
        while node:
            if self.check_morpheme(node):
                noun = node.surface
                if omit:
                    if self.check_unnecessary(noun) != None:
                        nouns.append(noun)
                else:
                    nouns.append(noun)
            node = node.next
        return nouns

    def noun_place(self, text):
        text = text.encode('utf-8')
        normalized = self.normalize(text)
        node = self.tagger.parseToNode(normalized)
        return self.extract_noun(node), self.extract_place(node)

    def parse(self, text, omit = True):
        text = text.encode('utf-8')
        normalized = self.normalize(text)
        node = self.tagger.parseToNode(normalized)
        nouns = []
        while node:
            if self.check_morpheme(node):
                noun = node.surface
                if omit:
                    if self.check_unnecessary(noun) != None:
                        nouns.append(noun)
                else:
                    nouns.append(noun)
            node = node.next
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
    			#print node.surface, ' : ', morphemeType
    			return False
    		
    	return test

    def check_unnecessary(self, noun):
        string = noun.decode('utf-8')
        kanji = re.search(u'[一-龠]', string)
        hiragana = re.search(u'[ぁ-ん]', string)
        katakana = re.search(u'[ァ-ヴ]', string)
        alphabet = re.search(u'[a-z]', string)
        
        if len(string) == 1:
            return None
        elif kanji == None and hiragana == None and katakana == None and alphabet == None:
            return None
        elif kanji == None and hiragana != None and katakana == None and alphabet == None and len(string) < 4:
            return None

        #if re.search(u'^[0-9]+(年|月|日)$', string)
        if re.search(u'^年度$', string):
        	return None
        if re.search(u'^([a-z]|[ぁ-ん]|[ァ-ヴ]|[一-龠]){4,}$', string):
        	return None
        	
        return noun
