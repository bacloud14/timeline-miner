from django import forms

class NameForm(forms.Form):
    your_text =  forms.CharField(
                    widget=forms.Textarea(attrs={
                        'cols': 200,
                        'rows': 3,
                        'style': 'width: 100%'
                    }),
                    required=True
                )