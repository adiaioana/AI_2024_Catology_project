from random import random
import pandas as pd
import random
from nltk.corpus import wordnet
import nltk
from actual_project.language_helper import get_race_in_short, race_to_num, get_race, numeric_to_string_data, \
    get_an_intro, isvowel, get_translation
from dataset_queries.dataset_upgrader import replaceStringWithNumeric, replaceUndefined
from labs.neuralNetwork import normalize, one_hot_encode
from labs.neuralNetwork import NeuralNetworkSigmoid
import numpy as np
from actual_project.predictRace import predictRaceFromDescription
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
reviews = pd.read_excel("D:\\FII\\AI\\Cat2\\input\\Data cat personality and predation Cordonnier et al.xlsx", index_col=0)

reviews= reviews.drop(columns=['Plus', 'Horodateur','Nombre'])
# dropped date column and 'how many cats in household' column as they're irrelevant

racesOrderedList = ['BEN','SBI','BRI','CHA','EUR','MCO','PER','RAG','SPH','ORI','TUV','Autre']

reviews = replaceStringWithNumeric(reviews)
reviews = replaceUndefined(reviews)
print(reviews)
'''
plotCorrelationMatrix(reviews, os.path.join('output_modelling','heatmaps'))
'''

'''
[<]
'''

'''
Generation of New Instances
'''

'''
print(
    'began demo model creation'
)
model = createCatRacePredictionDecisionTree(reviews)
print('began instance creation')
uniformInstances = generateInstancesUniform(100, reviews, model)
uniformMedianInstances = generateInstancesUniformMedian(100, reviews, model, 10 )


print(uniformInstances)
print(uniformMedianInstances)
'''
reviews= reviews.drop(columns=['Age', 'Sexe'])


numberOfRaces = reviews['Race'].nunique();
numberOfArguments = reviews.shape[1]-1;

reviewsX = reviews.drop(columns=['Race'], axis=1);
numpyReviewsX = reviews;
numpyReviewsX = numpyReviewsX.drop('Race', axis=1);
numpyReviewsX = numpyReviewsX.to_numpy();


#print(numpyReviewsX);
print('loading1...')

numpyReviewsY = reviews['Race'];
numpyReviewsY = numpyReviewsY.to_numpy().astype(int)-1;

#print(numpyReviewsY);
print('loading2...')

numpyReviewsX = normalize(numpyReviewsX);
numpyReviewsY = one_hot_encode(numpyReviewsY, numberOfRaces);

#print(numpyReviewsX);
#print(numpyReviewsY);
print('loading3...')



model = NeuralNetworkSigmoid([numberOfArguments, 8,8, numberOfRaces], 0.01);



permutation = np.random.permutation(numpyReviewsX.shape[0]);
numpyReviewsX = numpyReviewsX[permutation];
numpyReviewsY = numpyReviewsY[permutation];

trainX, testX = np.split(numpyReviewsX, [ int(0.8*numpyReviewsX.shape[0]) ]);
trainY, testY = np.split(numpyReviewsY, [ int(0.8*numpyReviewsX.shape[0])]);


model.train(trainX, trainY, testX, testY, 2, 100, 0.0);



modelWithoutHidden = NeuralNetworkSigmoid([numberOfArguments, numberOfRaces], 0.01);



permutation = np.random.permutation(numpyReviewsX.shape[0]);
numpyReviewsX = numpyReviewsX[permutation];
numpyReviewsY = numpyReviewsY[permutation];

trainX, testX = np.split(numpyReviewsX, [ int(0.8*numpyReviewsX.shape[0]) ]);
trainY, testY = np.split(numpyReviewsY, [ int(0.8*numpyReviewsX.shape[0])]);


modelWithoutHidden.train(trainX, trainY, testX, testY, 2, 100, 0.0);

''''''
def solver_description_to_cat_breed(text):
    race_short = predictRaceFromDescription(text, reviewsX, model)
    return get_race(race_short)
print(solver_description_to_cat_breed('This Bengal cat wihtin a household including an apartment with balcony or terrace, is in a periurban area, that spends a no time outside, spends a limited time with the owner, spread across moderate natural zones, it captures birds never, and like rarely for mammals, it captures birds never and and about rarely for mammal.'))
'''
sorry pycharm isn't working..
'''


FR_to_EN, EN_to_FR = get_translation()

def adj_EN():
    return list('Shy,Calm,Scared,Intelligent,Vigilant,Perseverant,Affectionate,Friendly,Lonely,Brutal,Dominant,Aggressive,Impulsive,Predictable,Distracted'.split(','))
def adj_FR():
    return list('Timide,Calme,Intelligent,Vigilant,Affectueux,Amical,Solitaire,Brutal,Dominant,Agressif,Impulsif,Distrait'.split(','))

def get_semi_phrases():
    attrs =[el for el in EN_to_FR.keys() if el != 'Time Clock' and el != 'Race' and el !='Number' and el not in adj_FR()]
    current_attr = ''

    word_to_fields = {key: [] for key in attrs}
    fp = open('D:/FII/AI/Cat2/text-generation/input-keys-to-sequences.txt', 'r')
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


def solver_race_to_description(race_long):
    fp = open('D:\\FII\\AI\\Cat2\\actual_project\\file_for_debugging.txt', 'w')
    df = reviews
    race=get_race_in_short(race_long)
    id_of_race = race_to_num(race)
    race_1_data = df[df['Race'] == id_of_race]
    race_1_average = race_1_data.mean().astype(int)
    race_1_entry = race_1_average.to_dict()
    phrase= get_phrase_from_entry(race_1_entry, race)
    fp.write(f'For the {race} with {id_of_race}:\n{phrase}\n\n')
    return phrase

def compare_breeds(race_long1, race_long2):

    race_in_short1=get_race_in_short(race_long1)
    race_in_short2=get_race_in_short(race_long2)
    fp =open('debug.txt', 'w')
    fp.write(race_in_short1)
    fp.write(race_in_short2)
    df = reviews
    race_1_data = df[df['Race'] ==  race_to_num(race_in_short1)]
    race_1_average = race_1_data.mean().astype(int)
    entry1 = race_1_average.to_dict()

    df = reviews
    race_2_data = df[df['Race'] ==  race_to_num(race_in_short2)]
    race_2_average = race_2_data.mean().astype(int)
    entry2 = race_2_average.to_dict()

    terms1 = [get_an_intro(race_in_short1)]
    terms2 = [get_an_intro(race_in_short2)]

    pred1 = []
    pred2 = []

    for key in entry1.keys():
        value1 = entry1[key]
        value2 = entry2.get(key, None)

        if FR_to_EN[key] != 'Sex' and FR_to_EN[key] in get_semi_phrases().keys():
            if len(get_semi_phrases()[FR_to_EN[key]]) > 0:
                term1 = random.choice(get_semi_phrases()[FR_to_EN[key]])
                term2 = random.choice(get_semi_phrases()[FR_to_EN[key]])

                new_term1 = transform_term(term1, numeric_to_string_data(key, value1))
                new_term2 = transform_term(term2, numeric_to_string_data(key, value2))

                terms1.append(new_term1)
                terms2.append(new_term2)

        if len(key) > 4 and key.lower()[:4] == 'pred':
            pred1.append((key, value1))
            if value2 is not None:
                pred2.append((key, value2))

    if len(pred1):
        terms1 += transform_pred(pred1)
    if len(pred2):
        terms2 += transform_pred(pred2)

    # Randomize the sentence structure for comparison
    comparison_structure = random.choice([
        "{0}'s {1} is {2}, while {3}'s {1} is {4}.",
        "{0} has {1} that {2}, whereas {3} displays {4}.",
        "Compared to {0}, which {1}, {3} {4}.",
        "In contrast to {0}, which {1}, {3} {4} more often.",
    ])

    # Randomly select phrases for both breeds
    phrase1 = " ".join(terms1[1:])
    phrase2 = " ".join(terms2[1:])

    phrase = comparison_structure.format(race_in_short1, "abundance", phrase1, race_in_short2, phrase2)

    return phrase
