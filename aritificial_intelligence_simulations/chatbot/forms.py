from django import forms

class IntentQuestions(forms.Form):
    name = forms.CharField(label='Your name', max_length=50)
    email = forms.EmailField()
    about = forms.CharField(label='About', widget=forms.Textarea)
    service_area = forms.CharField(label='Service Area', widget=forms.Textarea)