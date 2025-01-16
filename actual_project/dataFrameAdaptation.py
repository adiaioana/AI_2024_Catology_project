import pandas as pd

#adapts the data frame ( which doesn't contain the columns sexe, age, horodateour, nombre, )
def adaptDictionaryToDataFrameRow( review , realReviews ):
    newRealReviews = realReviews.copy();
    arr = [pd.DataFrame.from_dict(review, orient='columns'), newRealReviews];
    newReviews = pd.concat(arr);
    print(newReviews.iloc[[-1]]);
    return newReviews;