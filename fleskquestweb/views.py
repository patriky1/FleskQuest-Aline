import google.generativeai as genai
from django.shortcuts import render
from .forms import PerguntaForm
from django.conf import settings


# Configurar a chave da API do Google Gemini
genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)

# Defina o modelo de IA que será utilizado
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Texto pré-definido
texto_pre_definido = "você é um profissional em flaskquest e deve fazer uma análise detalhada sobre o tema:  "

# View que renderiza o template e processa a pergunta do usuário
def index(request):
    resposta = None
    pergunta = None

    if request.method == 'POST':
        form = PerguntaForm(request.POST)
        if form.is_valid():
            pergunta = form.cleaned_data['pergunta']
            # Adiciona o texto pré-definido à pergunta do usuário
            prompt = texto_pre_definido + pergunta
            try:
                # Utiliza o modelo para gerar a resposta
                response = model.generate_content(prompt)
                if response and response.text:
                    resposta = response.text
                else:
                    resposta = "Desculpe, não consegui gerar uma resposta."
            except Exception as e:
                resposta = f"Erro ao gerar resposta: {str(e)}"
    else:
        form = PerguntaForm()

    return render(request, 'index.html', {'form': form, 'pergunta': pergunta, 'resposta': resposta})
