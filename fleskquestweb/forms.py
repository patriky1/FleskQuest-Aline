from django import forms

class PerguntaForm(forms.Form):
    pergunta = forms.CharField(label='Faça sua pergunta', max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Digite sua pergunta...'
    }))