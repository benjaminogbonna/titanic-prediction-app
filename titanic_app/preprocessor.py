# Notebook's Import
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import FeatureUnion


# Preprocessing Pipeline
class DFSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.attribute_names]


# We will also need an imputer for the string categorical columns (the regular SimpleImputer does not work on those):
class MostFrequentImputer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.most_frequent_ = pd.Series([X[c].value_counts().index[0] for c in X],
                                        index=X.columns)
        return self

    def transform(self, X, y=None):
        return X.fillna(self.most_frequent_)


# pipeline for the numerical attributes:
num_pipeline = Pipeline([
        ("select_numeric", DFSelector(["Age", "SibSp"])),
        ("imputer", SimpleImputer(strategy="mean")),
    ])

# pipeline for the categorical attributes:
cat_pipeline = Pipeline([
        ("select_cat", DFSelector(["Pclass", "Sex"])),
        ("imputer", MostFrequentImputer()),
        ("cat_encoder", OneHotEncoder(sparse=False, handle_unknown = 'ignore')),
    ])

# Finally, let's join the numerical and categorical pipelines:
preprocess_pipeline = FeatureUnion(
    transformer_list=[
        ("num_pipeline", num_pipeline),
        ("cat_pipeline", cat_pipeline),
    ])
