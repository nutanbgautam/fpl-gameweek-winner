from django import forms

class LeagueId(forms.Form):
    attrs = {
        "type": "password"
    }
    email=forms.CharField()
    password=forms.CharField(widget=forms.TextInput(attrs=attrs))
    leagueId=forms.CharField()