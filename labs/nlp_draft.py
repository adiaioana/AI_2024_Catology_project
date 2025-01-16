import os
import sys
import random
from langdetect import detect
from collections import Counter
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet as wn
import nltk
from yake import KeywordExtractor


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


romanian_stopwords = frozenset(stopwords.words('romanian'))


def get_text(input_source):
    return open(input_source, 'r', encoding='utf-8').read() if os.path.isfile(input_source) else input_source


def identify_language(content):
    return detect(content)


def analyze_stylometry(content):
    tokens = word_tokenize(content)
    total_chars = len(content)
    total_words = len(tokens)
    word_frequencies = Counter(token.lower() for token in tokens if token.isalnum() and token.lower() not in romanian_stopwords)
    return {
        'num_words': total_words,
        'num_chars': total_chars,
        'word_frequencies': word_frequencies
    }


def create_alternative_version(content, replace_fraction=0.2):
    words = word_tokenize(content)
    count_to_replace = int(len(words) * replace_fraction)
    replace_indices = random.sample(range(len(words)), count_to_replace)
    updated_words = words[:]

    for i in replace_indices:
        potential_synsets = wn.synsets(words[i], lang='ron')
        if potential_synsets:
            synonyms = {lemma.name() for synset in potential_synsets for lemma in synset.lemmas('ron') if lemma.name() != words[i]}
            hypernyms = {lemma.name() for synset in potential_synsets for hyper in synset.hypernyms() for lemma in hyper.lemmas('ron')}
            antonyms = {f"ne{lemma.name()}" for synset in potential_synsets for lemma in synset.lemmas('ron') for antonym in lemma.antonyms()}
            possible_replacements = synonyms | hypernyms | antonyms
            if possible_replacements:
                updated_words[i] = random.choice(list(possible_replacements))

    return ' '.join(updated_words)


def keyword_sentences(content):
    kw_extractor = KeywordExtractor(lan="ro", n=1, top=10)
    keywords = kw_extractor.extract_keywords(content)
    relevant_sentences = []

    for kw, _ in keywords:
        for sentence in sent_tokenize(content):
            if kw in sentence:
                relevant_sentences.append(sentence)
                relevant_sentences.append(dummy_similar_sentence(sentence,kw))
                break

    return relevant_sentences


def dummy_similar_sentence(sentence,kw):
    words = word_tokenize(sentence)
    updated_words = words[:]
    replaced = False  # Indicator pentru a verifica dacă am înlocuit un cuvânt

    for i, word in enumerate(words):
        if not word.isalpha() or len(word) <= 2:
            continue
        if word == kw:
            continue

        potential_synsets = wn.synsets(word, lang='ron')
        if potential_synsets:
            synonyms = {lemma.name() for synset in potential_synsets for lemma in synset.lemmas('ron') if
                        lemma.name() != word}
            if synonyms:
                updated_words[i] = random.choice(list(synonyms))
                replaced = True

    if not replaced:
        for i, word in enumerate(words):
            if word != kw:
                potential_synsets = wn.synsets(word, lang='ron')
                if potential_synsets:
                    synonyms = {lemma.name() for synset in potential_synsets for lemma in synset.lemmas('ron') if
                                lemma.name() != word}
                    if synonyms:
                        updated_words[i] = random.choice(list(synonyms))
                        break

    return ' '.join(updated_words)

if _name_ == "_main_":
    if len(sys.argv) < 2:
        print("Mod utilizare: python script.py <cale_sau_text>")
        sys.exit(1)

    fp = open('nlp_output.txt', 'w', encoding='utf-8')
    text_input = get_text(sys.argv[1])

    detected_language = identify_language(text_input)
    print(f"Limba identificata: {detected_language}")
    fp.write(f"Limba identificata: {detected_language}\n")

    stylometry_data = analyze_stylometry(text_input)
    print(f"Numar cuvinte: {stylometry_data['num_words']}")
    print(f"Numar caractere: {stylometry_data['num_chars']}")
    print("Cele mai frecvente cuvinte:")
    fp.write(f"Numar cuvinte: {stylometry_data['num_words']}"+'\n'+f"Numar caractere: {stylometry_data['num_chars']}"+'\n'+'Cele mai frecvente cuvinte:\n')
    for word, freq in stylometry_data['word_frequencies'].most_common(10):
        print(f"{word}: {freq}")
        fp.write(f"{word}: {freq}\n")

    alternative_version = create_alternative_version(text_input)
    print("\nText alternativ generat:")
    fp.write(f'\nText alternativ generat:\n{alternative_version}\n')
    print(alternative_version)

    keyword_based_sentences = keyword_sentences(text_input)
    print("\nPropozitii bazate pe cuvinte cheie:")
    fp.write("\nPropozitii bazate pe cuvinte cheie:\n")
    for sentence in keyword_based_sentences:
        print(sentence)
        fp.write(sentence+'\n')
