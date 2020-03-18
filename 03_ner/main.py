# -*- coding: utf-8 -*-
"""

Filename: main.py

Author:   Ednalyn C. De Dios
Phone:    (210) 236-2685
Email:    ednalyn.dedios@taskus.com 

Created:  March 13, 2020
Updated:  March 14, 2020

PURPOSE: conduct nlp on a one-column flat file.

PREREQUISITES: txtdata in the first row of the data.

DON'T FORGET TO:
1. Hydrate.
2. Sleep.
3. Have fun!

"""

# import os
# os.environ["KIVY_NO_CONSOLELOG"] = "1"

import pandas as pd

import tkinter as tk
from tkinter import filedialog

# natural language processing: n-gram ranking
import re
import unicodedata
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords

# add appropriate words that will be ignored in the analysis
ADDITIONAL_STOPWORDS = ['campaign']

# for natural language processing: named entity recognition
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty



class MyGrid(Widget):

    def __init__(self, **kwargs): 
  
        # The super() builtin 
        # returns a proxy object that 
        # allows you to refer parent class by 'super'.  
        super(MyGrid, self).__init__(**kwargs)

    def clean(self, text):
        """
        A simple function to clean up the data. All the words that
        are not designated as a stop word is then lemmatized after
        encoding and basic regex parsing are performed.
        """
        wnl = nltk.stem.WordNetLemmatizer()
        stopwords = nltk.corpus.stopwords.words('english') + ADDITIONAL_STOPWORDS
        text = (unicodedata.normalize('NFKD', text)
        .encode('ascii', 'ignore')
        .decode('utf-8', 'ignore')
        .lower())
        words = re.sub(r'[^\w\s]', '', text).split()
        return [wnl.lemmatize(word) for word in words if word not in stopwords]

    def btn_close(self):
        App.get_running_app().stop()

    def load_file(self,filepath):
        self.ti_output.text = filepath
        df = pd.read_csv(filepath, encoding='Latin_1')
        # clean and tokenize
        content_list = df.txtdata.tolist()
        global CONTENT
        global ARTICLE
        CONTENT = self.clean(''.join(str(content_list)))
        # named entity recognition
        ARTICLE = nlp(' '.join(df.txtdata.tolist()))

        self.ti_message.text = "File loaded. Click on any of the function buttons on the right to analyze the text. 2=bigrams, 3=trigrams, 4=qualgrams, others=entities. CLOSE= close this app."

    def get_bigrams(self):
        # bigrams
        bigrams = (pd.Series(nltk.ngrams(CONTENT, 2)).value_counts())[:40].to_dict()
        self.ti_output.text = str(bigrams)

    def get_trigrams(self):
        # trigrams
        trigrams = (pd.Series(nltk.ngrams(CONTENT, 3)).value_counts())[:40].to_dict()
        self.ti_output.text = str(trigrams)
    
    def get_qualgrams(self):
        # qualgrams
        qualgrams = (pd.Series(nltk.ngrams(CONTENT, 4)).value_counts())[:40].to_dict()
        self.ti_output.text = str(qualgrams)

    def ner_person(self):
        # person: people, including fictional characters
        person_list = []
        for ent in ARTICLE.ents:
            if ent.label_ == 'PERSON':
                person_list.append(ent.text)
        person = pd.DataFrame(Counter(person_list).most_common(40), columns=['entity', 'count']).to_dict()
        self.ti_output.text = str(person)

    def ner_group(self):
        # norp: nationalities or religious or political groups
        norp_list = []
        for ent in ARTICLE.ents:
            if ent.label_ == 'NORP':
                norp_list.append(ent.text)
        group = pd.DataFrame(Counter(norp_list).most_common(40), columns=['entity', 'count']).to_dict()
        self.ti_output.text = str(group)

    def ner_org(self):
        # org: companies, agencies, institutions, etc
        org_list = []
        for ent in ARTICLE.ents:
            if ent.label_ == 'ORG':
                org_list.append(ent.text)
        org = pd.DataFrame(Counter(org_list).most_common(40), columns=['entity', 'count']).to_dict()
        self.ti_output.text = str(org)

    def ner_geo(self):
        # gpe: countries, cities, states
        geo_list = []
        for ent in ARTICLE.ents:
            if ent.label_ == 'GPE':
                geo_list.append(ent.text)
        geo = pd.DataFrame(Counter(geo_list).most_common(40), columns=['entity', 'count']).to_dict()
        self.ti_output.text = str(geo)

    def ner_product(self):
        # product: objects, vehicles, foods, etc. (Not services.) 
        product_list = []
        for ent in ARTICLE.ents:
            if ent.label_ == 'PRODUCT':
                product_list.append(ent.text)
        product = pd.DataFrame(Counter(product_list).most_common(40), columns=['entity', 'count']).to_dict()
        self.ti_output.text = str(product)

    def ner_event(self):
        # event: named hurricanes, battles, wars, sports events, etc 
        event_list = []
        for ent in ARTICLE.ents:
            if ent.label_ == 'EVENT':
                event_list.append(ent.text)
        event = pd.DataFrame(Counter(event_list).most_common(40), columns=['entity', 'count']).to_dict()
        self.ti_output.text = str(event)



class PathButton(Button):
    @staticmethod
    def get_path():
        root = tk.Tk()
        root.withdraw()
        return(filedialog.askopenfilename())



class PlaylistApp(App):
    def build(self):
        return MyGrid()


if __name__ == '__main__':
    PlaylistApp().run()