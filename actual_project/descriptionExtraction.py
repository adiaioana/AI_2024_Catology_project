import spacy
from spacy.matcher import Matcher
import pandas as pd

def extract_cat_attributes(text):
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Initialize attributes with ['NSP']
    attributes = {
        "Logement": [0],
        "Zone": [0],
        "Ext": [0],
        "Obs": [0],
        "Abondance": [0],
        "PredOiseau": [0],
        "PredMamm": [0],
        "Timide": [0],
        "Calme": [0],
        "Effrayé": [0],
        "Intelligent": [0],
        "Vigilant": [0],
        "Perséverant": [0],
        "Affectueux": [0],
        "Amical": [0],
        "Solitaire": [0],
        "Brutal": [0],
        "Dominant": [0],
        "Agressif": [0],
        "Impulsif": [0],
        "Prévisible": [0],
        "Distrait": [0],
    }

    # Define mapping from text descriptions to numerical values
    value_map = {
        "urban":1,
        "periurban":2,
        "rural":3,
        "none": 1,
        "limited": 2,
        "moderate": 3,
        "long": 4,
        "all": 5,
        "low": 1,
        "moderate": 2,
        "high": 3,
        "never": 1,
        "rarely": 2,
        "sometimes": 3,
        "often": 4,
        "very often": 5,
        "shy": 3,
        "calm": 3,
        "frightened": 3,
        "intelligent": 3,
        "vigilant": 3,
        "perseverant": 3,
        "affectionate": 3,
        "friendly": 3,
        "solitary": 3,
        "brutal": 3,
        "dominant": 3,
        "aggressive": 3,
        "impulsive": 3,
        "predictable": 3,
        "distracted": 3,
    }

    # Define patterns for Matcher
    matcher = Matcher(nlp.vocab)

    patterns = {
        #"Logement": [[{"LOWER": "apartment"}, {"LOWER": {"IN": ["without", "with"]}}, {"LOWER": {"IN": ["balcony", "terrace"]}}],
         #            [{"LOWER": "house"}, {"LOWER": {"IN": ["in", "without"]}}, {"LOWER": "subdivision"}]],
        "Zone": [[{"LOWER": {"IN": ["urban", "periurban", "rural"]}}]],
        "Ext": [[{"LOWER": {"IN": ["none", "limited", "moderate", "long", "all"]}}, {"LOWER": "time"}, {"LOWER": "outdoors"}]],
        "Obs": [[{"LOWER": {"IN": ["none", "limited", "moderate", "long"]}}, {"LOWER": "time"}, {"LOWER": "with"}, {"LOWER": "the"}, {"LOWER": "cat"}]],
        "Abondance": [[{"LOWER": {"IN": ["low", "moderate", "high"]}}, {"LOWER": "abundance"}]],
        "PredOiseau": [[{"LOWER": {"IN": ["never", "rarely", "sometimes", "often", "very"]}}, {"LOWER": "captures"}, {"LOWER": "birds"}]],
        "PredMamm": [[{"LOWER": {"IN": ["never", "rarely", "sometimes", "often", "very"]}}, {"LOWER": "captures"}, {"LOWER": "mammals"}]],
        # Personality attributes
        "Timide": [[{"LOWER": "shy"}]],
        "Calme": [[{"LOWER": "calm"}]],
        "Effrayé": [[{"LOWER": "frightened"}]],
        "Intelligent": [[{"LOWER": "intelligent"}]],
        "Vigilant": [[{"LOWER": "vigilant"}]],
        "Perséverant": [[{"LOWER": "perseverant"}]],
        "Affectueux": [[{"LOWER": "affectionate"}]],
        "Amical": [[{"LOWER": "friendly"}]],
        "Solitaire": [[{"LOWER": "solitary"}]],
        "Brutal": [[{"LOWER": "brutal"}]],
        "Dominant": [[{"LOWER": "dominant"}]],
        "Agressif": [[{"LOWER": "aggressive"}]],
        "Impulsif": [[{"LOWER": "impulsive"}]],
        "Prévisible": [[{"LOWER": "predictable"}]],
        "Distrait": [[{"LOWER": "distracted"}]],
    }

    # Add patterns to matcher
    for key, value in patterns.items():
        matcher.add(key, value)

    # Apply matcher to doc
    matches = matcher(doc)

    # Extract matched attributes
    for match_id, start, end in matches:
        match_text = doc[start:end].text.lower().split(' ')[0]
        for attribute in attributes:
            if nlp.vocab.strings[match_id] == attribute:
                attributes[attribute] = [int(value_map.get(match_text, match_text))]  # Map text to numerical value if available
    print(attributes);
    return attributes

"""
# Example text
description = "
The cat lives in an apartment with a balcony. It resides in an urban area. It spends limited time outdoors, less than an hour daily. The owner spends moderate time, 1 to 5 hours, with the cat. The area around has a moderate abundance of natural areas. The cat rarely captures birds, about 1 to 5 times a year, and never captures small mammals. It is shy, calm, frightened, intelligent, vigilant, perseverant, affectionate, friendly, solitary, brutal, dominant, aggressive, impulsive, predictable, and distracted.
"

# Extract attributes
attributes = extract_cat_attributes(description)
print(attributes)
print( pd.DataFrame.from_dict(attributes, orient='columns') );

text = input('cat description: ');
print( extract_cat_attributes(text) );

"""