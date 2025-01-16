from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
from sklearn import utils


def createCatRacePredictionDecisionTree(df):
    X = df.drop(['Race'], axis=1)

    y = df['Race'];

    lab_enc = preprocessing.LabelEncoder()
    encoded = lab_enc.fit_transform(y)
    y = encoded;

    catRacePredictionDecisionTree = DecisionTreeClassifier(criterion='entropy', max_depth=8, random_state=0);
    catRacePredictionDecisionTree.fit(X, y);

    return catRacePredictionDecisionTree;