import random


def numeric_to_string_data(attr, num):
    print(attr,num)
    all_data ={
        'Sex': {0:'M', 1:'F'},
        'Age':{1:'<1',2:'1-2',3:'2-10',4:'>10'},
        'Obs':{1:'none',2:'limited',3:'moderate',4:'long',5:'all the time'},
        'Ext':{1:'none',2:'limited',3:'moderate',4:'long',5:'all the time'},
        'Logement':{1:'apartment without balcony',2:'apartment with balcony or terrace',3:'house in a subdivision',4:'individual house'},
        'Zone':{1:'urban',2:'periurban',3:'rural'},
        'Abondance': {1:'low', 2:'moderate', 3: 'high'},
        'Pred':{1:'never',2:'rarely',3:'sometimes',4:'often',5:'very often'}
    }
    if attr.lower().find('pred')>=0:
        return all_data['Pred'][num]
    if attr.lower() in [word.lower() for word in all_data.keys()]:
        return all_data[attr][num]
    print(f"Attribute {attr} not found in all data")
    return ' '
def get_an_intro(race_in_short):
    intros = ['This <...> cat',
              'This cat of breed <...>',
              'This feline companion of breed <...>',
              'This particular cat of breed <...>',
              'This <...> feline',
              'This cat which is <...>',
              'This beloved <...> cat']
    term = intros[random.randint(0, len(intros) - 1)]
    term = term[:term.find('<')] + get_race(race_in_short) + term[term.find('>') + 1:]
    return term
def isvowel(ch):
    return True if ch in 'aeiouAEIOU' else False



def get_translation():
    fp = open('D:\\FII\\AI\\Cat2\\text-generation\\translation.txt', 'r')
    line1 =fp.readline()
    line2 = fp.readline()
    key_words, key_values =line1.split(','), line2.split(',')
    key_words[-1] = key_words[-1].strip()
    key_values[-1] = key_values[-1].strip()
    FR_to_EN1 = ({key_words[ind]:key_values[ind] for ind in range(len(key_words))}
                 | {'Prévisible':'Predictable', 'Perséverant':'Perseverant','Effrayé':'Scared'})
    EN_to_FR1 = ({key_values[ind]:key_words[ind] for ind in range(len(key_words))}
                 | {'Predictable':'Prévisible','Perseverant':'Perséverant','Scared':'Effrayé'})
    return FR_to_EN1, EN_to_FR1

def get_race(race_short):
    all_races ='Bengal/Birman/British Shorthair/Chartreux/European/Maine coon/Persian/ Ragdoll/Savannah/Sphynx/Siamese/Turkish angora/unknown breed/'.split('/')
    races = 'BEN/SBI/BRI/CHA/EUR/MCO/PER/RAG/SPH/ORI/TUV/Autre/NSP'.split('/')
    races_lower = 'BEN/SBI/BRI/CHA/EUR/MCO/PER/RAG/SPH/ORI/TUV/Autre/NSP'.lower().split('/')
    return all_races[races_lower.index(race_short.lower())]
def get_race_in_short(race_long):
    all_races = 'Bengal/Birman/British Shorthair/Chartreux/European/Maine coon/Persian/ Ragdoll/Savannah/Sphynx/Siamese/Turkish angora/unknown breed/'.split('/')
    all_races_lower ='Bengal/Birman/British Shorthair/Chartreux/European/Maine coon/Persian/Ragdoll/Savannah/Sphynx/Siamese/Turkish angora/unknown breed/'.lower().split('/')
    races = 'BEN/SBI/BRI/CHA/EUR/MCO/PER/RAG/SPH/ORI/TUV/Autre/NSP'.split('/')
    return races[all_races_lower.index(race_long.lower())]
def race_to_num(race):
    map ={
                'BEN': 1,
                'SBI': 2,
                'BRI': 3,
                'CHA': 12,
                'EUR': 5,
                'MCO': 6,
                'PER': 7,
                'RAG': 8,
                'SPH': 9,
                'ORI': 4,
                'TUV': 11,
                'Autre': 10}
    return map[race]
'''
map = {
        'Ext': {
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5
        },
        'Obs': {
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            1: 1,
            2: 2,
            3: 3,
            4: 4
        },
        'Abondance': {
            '1': 1,
            '2': 2,
            '3': 3,
        },
        'PredOiseau': {
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5
        },
        'PredMamm': {
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5
        },
        'Sexe':
            {'M': 0,
             'F': 1},
        'Age':
            {'Moinsde1': 1,
             '1a2': 2,
             '2a10': 3,
             'Plusde10': 4
             }
        ,

        'Race':
            {
                'BEN': 1,
                'SBI': 2,
                'BRI': 3,
                'CHA': 12,
                'EUR': 5,
                'MCO': 6,
                'PER': 7,
                'RAG': 8,
                'SPH': 9,
                'ORI': 4,
                'TUV': 11,
                'Autre': 10
            }
        ,

        'Logement':
            {'ASB': 1,
             'AAB': 2,
             'ML': 3,
             'MI': 4},

        'Zone':
            {'U': 1,
             'PU': 2,
             'R': 3}

'''