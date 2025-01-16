import numpy as np
import pandas as pd
'''
Adding new generated instances to dataset
'''
def generateInstancesUniform(numberOfInstances,df, model):
    resultDf = pd.DataFrame();
    for column in df.columns:
        if(column!='Race'):
            #print(column);
            #print( (df.sample(n=1))[column].values[0] );
            resultDf.insert( resultDf.columns.size, column, [(df.sample(n=1))[column].values[0] for _ in range(numberOfInstances) ] , True );

    race = model.predict(resultDf);

    resultDf.insert( 0, 'Race', race, True );

    return resultDf;

def generateInstancesUniformMedian(numberOfInstances, df,model, numberOfRpetitions):
    resultDf = pd.DataFrame();
    for column in df.columns:
        if(column!='Race'):
            #print(column);
            resultDf.insert( resultDf.columns.size, column, [ np.median( np.array( [(df.sample(n=1))[column].values[0] for __ in range(numberOfRpetitions)] ) ) for _ in range(numberOfInstances) ]  , True );

    race = model.predict(resultDf);

    resultDf.insert(0, 'Race', race, True);

    return resultDf;

'''
Data replacing:
    - with numeric values
    - Unknown values => Mean of attribute
'''

def replaceUndefined(df):
    for col in df.columns:
        means = df[col].mean();
        print(means);
        df[col] = df[col].replace('NSP', means)
        df[col] = df[col].fillna(means);
        df[col] = df[col].replace(np.nan, means);
        df[col] = df[col].replace('NaN', means);
        means = df[col].mean()
        df[col] = df[col].replace('NSP', means)
    return df


def replaceStringWithNumeric(df):
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

    }

    for column in map.keys():
        if(column not in df.columns):continue

        df[column] = df[column].map(map[column])
        if not pd.notna(df[column].mean()):
            print(column)
            continue
        mean = int(df[column].mean())
        df[column] = df[column].fillna(mean)

    return df
