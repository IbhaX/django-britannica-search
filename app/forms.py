from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your search", "name": "search"})
    )
    
    search.label = ""
