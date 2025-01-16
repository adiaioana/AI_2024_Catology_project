'''
    Generating a description using a classification based on the initial database.
    Generating phrases using bits of texts from the
'''
from random import random
import pandas as pd
import random

from dataset_queries.dataset_upgrader import replaceStringWithNumeric, replaceUndefined
from language_helper import numeric_to_string_data, race_to_num, get_an_intro, get_translation, isvowel
from nltk.corpus import wordnet
import nltk

def get_final_db():
    db = pd.read_excel("../input/Data cat personality and predation Cordonnier et al.xlsx", index_col=0)#,encoding='iso-8859-1')
    db= db.drop(columns=['Plus', 'Horodateur','Nombre']) # dropped date column and 'how many cats in household' column as they're irrelevant

    db = replaceStringWithNumeric(db)
    db = replaceUndefined(db)
    return db

df = get_final_db()

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

FR_to_EN, EN_to_FR = get_translation()

def adj_EN():
    return list('Shy,Calm,Scared,Intelligent,Vigilant,Perseverant,Affectionate,Friendly,Lonely,Brutal,Dominant,Aggressive,Impulsive,Predictable,Distracted'.split(','))
def adj_FR():
    return list('Timide,Calme,Intelligent,Vigilant,Affectueux,Amical,Solitaire,Brutal,Dominant,Agressif,Impulsif,Distrait'.split(','))

def get_semi_phrases():
    attrs =[el for el in EN_to_FR.keys() if el != 'Time Clock' and el != 'Race' and el !='Number' and el not in adj_FR()]
    current_attr = ''

    word_to_fields = {key: [] for key in attrs}
    fp = open('../text-generation/input-keys-to-sequences.txt', 'r')
    for line in fp.readlines():
        line = line[:line.find('\n')]
        if line.find('/')>=0:
            current_attr = ''
        elif line in FR_to_EN.keys():
            current_attr = line
        elif current_attr != '':
            word_to_fields[FR_to_EN[current_attr]].append(line)
    return word_to_fields

def transform_term(uncompl_term, str_value):
    new_term = uncompl_term[:uncompl_term.find('<')]
    if uncompl_term.find('!')>=0:
        new_term=new_term +('an' if isvowel(str_value[0]) else 'a') + ' '
    if str_value.lower() == 'none':
       str_value = 'no'
    new_term = new_term + str_value + uncompl_term[uncompl_term.find('>') + 1:]
    return new_term

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return list(set(synonyms))

def transform_pred(pred_pairs):
    terms = []
    if len(pred_pairs)>1:
        for pair in pred_pairs:
            key, value= pair[0], pair[1]
            term = get_semi_phrases()[FR_to_EN[key]][random.randint(0, len(get_semi_phrases()[FR_to_EN[key]]) - 1)]
            new_term = transform_term(term, numeric_to_string_data(key, value))
            terms.append(new_term)
        return terms
    for i in range(len(terms)):
        a= random.randint(0,2)
        if a == 1:
            terms[i] =random.choice(get_synonyms(terms[i]))
    return terms

def get_phrase_from_entry(entry, race_in_short):
    terms= [get_an_intro(race_in_short)]
    print(get_semi_phrases().keys())
    pred =[]
    for key in entry.keys(): # keys are in french
        value = entry[key]
        if FR_to_EN[key]!='Sex' and FR_to_EN[key] in get_semi_phrases().keys():
            if len(get_semi_phrases()[FR_to_EN[key]]) > 0:
                term = get_semi_phrases()[FR_to_EN[key]][random.randint(0,len(get_semi_phrases()[FR_to_EN[key]])-1)]
                new_term = transform_term(term, numeric_to_string_data(key,value))
                terms.append(new_term)
        if len(key)>4 and key.lower()[:4]=='pred':
            pred.append((key,value))

    if len(pred):
        terms += transform_pred(pred)
    phrase = terms[0] + ' '
    for index in range(1,len(terms)):
        phrase = phrase + terms[index]
        if index == len(terms)-2:
            phrase = phrase + ' and '
        elif len(terms)-2 > index > 0:
            phrase = phrase + ', '
        else:
            phrase = phrase + '.'

    return phrase


def get_phrase_from_entry(entry, race_in_short):
    terms= [get_an_intro(race_in_short)]
    print(get_semi_phrases().keys())
    pred =[]
    for key in entry.keys(): # keys are in french
        value = entry[key]
        if FR_to_EN[key]!='Sex' and FR_to_EN[key] in get_semi_phrases().keys():
            if len(get_semi_phrases()[FR_to_EN[key]]) > 0:
                term = get_semi_phrases()[FR_to_EN[key]][random.randint(0,len(get_semi_phrases()[FR_to_EN[key]])-1)]
                new_term = transform_term(term, numeric_to_string_data(key,value))
                terms.append(new_term)
        if len(key)>4 and key.lower()[:4]=='pred':
            pred.append((key,value))

    if len(pred):
        terms += transform_pred(pred)
    phrase = terms[0] + ' '
    for index in range(1,len(terms)):
        phrase = phrase + terms[index]
        if index == len(terms)-2:
            phrase = phrase + ' and '
        elif len(terms)-2 > index > 0:
            phrase = phrase + ', '
        else:
            phrase = phrase + '.'

    return phrase


def tester():
    fp = open('file_for_testing.txt', 'w')
    races = 'BEN/SBI/BRI/CHA/EUR/MCO/PER/RAG/SPH/ORI/TUV'
    for race in races.split('/'):
        fp.write(f'Senteces for {race}>\n\n')
        id_of_race = race_to_num(race)
        # Filter rows where Race equals 1
        race_1_data = df[df['Race'] == id_of_race]

        # Compute the average for each column
        race_1_average = race_1_data.mean().astype(int)

        # Convert to a dictionary or keep it as a pandas Series
        race_1_entry = race_1_average.to_dict()

        # Display the entry
        fp.write(f'1> {get_phrase_from_entry(race_1_entry, race)}')
        fp.write('\n')
        fp.write(f'2> {get_phrase_from_entry(race_1_entry, race)}')
        fp.write('\n')
        fp.write(f'3> {get_phrase_from_entry(race_1_entry, race)}')
        fp.write('\n')

import random


