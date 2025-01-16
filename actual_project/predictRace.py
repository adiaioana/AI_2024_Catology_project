from actual_project.dataFrameAdaptation import adaptDictionaryToDataFrameRow
from actual_project.descriptionExtraction import extract_cat_attributes
from labs.neuralNetwork import normalize
import numpy as np

racesOrderedList = ['BEN','SBI','BRI','CHA','EUR','MCO','PER','RAG','SPH','ORI','TUV','Autre']
def getRaceFromPrediction(prediction):
    return racesOrderedList[ np.argmax( np.array(prediction[0]) ) ];

def predictRaceFromDescription(text, reviews, model):
    dict = extract_cat_attributes(text);
    newReviews = adaptDictionaryToDataFrameRow(dict, reviews);
    numpyReviewsX = normalize(newReviews);
    numpyReviewsX = numpyReviewsX[-1:];
    print(numpyReviewsX);
    return getRaceFromPrediction( model.forward(numpyReviewsX) );

