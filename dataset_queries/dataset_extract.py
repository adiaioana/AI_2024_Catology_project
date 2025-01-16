'''
Getting duplicates/value counts
'''

def get_value_counts(df, fp):
    for column in df.columns:
        counts = df[column].value_counts()
        fp.write(f'{counts.to_string()}\n_______________________\n')

def write_duplicates(df):
    which_are_duplicates = df[df.duplicated(keep=False)]
    fp = open('../output_modelling/detected_duplicates.txt', 'w+')
    fp.write('Duplicate rows are')
    fp.write(f'{which_are_duplicates.to_string()}')
    fp.close()

def write_missing_or_unknown(df):
    missing_values = df.isnull().stack()
    missing_pairs = missing_values[missing_values].index.tolist()

    nsp_values = df == "NSP"
    nsp_pairs = nsp_values.stack()[nsp_values.stack()].index.tolist()
    fp = open('../output_modelling/detected_nsp_pairs.txt', 'w+')
    fp.write('NSP(or Unknown values) elements are\n')
    for pair in nsp_pairs:
        fp.write(f'{pair}\n')
    fp.close()


def calculate_frequencies_by_race(df, race_column):
    frequencies = {}

    for race, group in df.groupby(race_column):
        race_freqs = {}

        for col in df.columns:
            if col != race_column :
                race_freqs[col] = group[col].value_counts()

        frequencies[race] = race_freqs

    return frequencies

def write_race_and_attr_counts(df):
    fp = open('../output_modelling/race_counts.txt', 'w+')

    #fp.write(f'{df[["Race"]].value_counts().to_string()}\n')
    race_frequencies = calculate_frequencies_by_race(df, 'Race')

    for race, freq in race_frequencies.items():
        fp.write(f"Frequencies for Race: {race}")
        for attribute, counts in freq.items():
            fp.write(f"\n{counts.to_string()}")
    fp.close()

    fp = open('../output_modelling/attr_counts.txt', 'w+')
    get_value_counts(df, fp)
    fp.close()