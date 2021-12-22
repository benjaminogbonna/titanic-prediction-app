from django import forms

GENDER_CHOICE = (
    ("female", "Female"),
    ("male", "Male"),
)
CLASS_CHOICE = (
    (1, 1),
    (2, 2),
    (3, 3),
)


class Checker(forms.Form):
    name = forms.CharField(label='Name',
                           max_length=100,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Enter name'
                           }))
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICE)
    age = forms.CharField(label='Age', max_length=4,
                          widget=forms.TextInput(attrs={
                              'placeholder': '1-100'
                          }))
    class_ = forms.ChoiceField(label='Class', choices=CLASS_CHOICE)
    siblings = forms.CharField(label='Siblings', max_length=4,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Number of siblings on board'
                               }))
