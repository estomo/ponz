# -*- coding: utf-8 -*-
import logging
from gensim import corpora, models, similarities

import MeCab
import unicodedata
import re

class TopicModel:

    def __init__(self):
        self.tagger = MeCab.Tagger("-Ochasen")

    def parse(self, text, omit = True):
        return nouns

