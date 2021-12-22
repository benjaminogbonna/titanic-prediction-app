from django.shortcuts import render
# from django.http import HttpResponse  # Http404, HttpResponseRedirect
# from django.template import loader
# from django.urls import reverse
# from django.views import generic
from .forms import Checker
import os
import pandas as pd
import joblib
from sklearn.pipeline import FeatureUnion
from . import preprocessor as ps


# preparing the Classifier
cur_dir = os.path.dirname(__file__)
clf = joblib.load(os.path.join(cur_dir, 'pickled', 'forest.joblib'))

preprocess_pipeline = FeatureUnion(
    transformer_list=[
        ("num_pipeline", ps.num_pipeline),
        ("cat_pipeline", ps.cat_pipeline),
    ])
data = os.path.join(cur_dir, 'data', 'train.csv')
new_data = os.path.join(cur_dir, 'data', 'new_data.csv')
X_train = preprocess_pipeline.fit_transform(pd.read_csv(data))


# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Checker(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cd = form.cleaned_data
            # process the data in form.cleaned_data as required
            new_df = pd.DataFrame({'Sex': [cd['gender']],
                                   'Pclass': int(cd['class_']),
                                   'Age': int(cd['age']),
                                   'SibSp': int(cd['siblings']),
                                   })

            x_new = preprocess_pipeline.transform(new_df)
            prediction = clf.predict(x_new)
            name = cd['name']
            if prediction == 0:
                result = f'Wooo 😮 {name.title()}, you Died 😢'
            else:
                result = f'Cheers 🥂 {name.title()}, you Survived 😁'

            context = {
                'prediction': result,
                'form': form,
            }
            with open(new_data, 'a') as file:
                file.write(f"{name},{cd['gender']},{cd['age']},{cd['class_']},{cd['siblings']},{prediction[0]}\n")

            return render(request,
                          'titanic_app/index.html', context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Checker()
    return render(request, 'titanic_app/index.html', {'form': form})
