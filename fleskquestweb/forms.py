from django import forms

class PerguntaForm(forms.Form):
    pergunta = forms.CharField(
        label='Faça sua pergunta',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control my-custom-class',  # Adicione várias classes se necessário
            'placeholder': 'Digite sua pergunta...',
            'style': 'border: 2px solid #00aaff; padding: 10px; font-size: 16px; margin: 15px;'  # CSS inline personalizado
        })
    )
