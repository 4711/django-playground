from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(label='bla',
        widget=forms.TextInput(attrs={'size': 32})
    )
