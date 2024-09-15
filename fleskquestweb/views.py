import google.generativeai as genai
from django.shortcuts import render
from .forms import PerguntaForm
from django.conf import settings
import json
# import markdown
# register = template.Library()
# Configurar a chave da API do Google Gemini
genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)

# Defina o modelo de IA que será utilizado
model = genai.GenerativeModel("gemini-1.5-flash-latest", generation_config={"response_mime_type": "application/json"})

# Texto pré-definido
texto_pre_definido = "você é um profissional em flaskquest e deve fazer uma análise detalhada sobre o tema:  "



def index(request):
    if 'conversas' not in request.session:
        request.session['conversas'] = []  # Inicializa o histórico de conversa na sessão

    resposta = None
    pergunta = None

    if request.method == 'POST':
        if 'limpar_conversa' in request.POST:
            # Limpar a conversa ao detectar o botão "Limpar Conversa"
            request.session['conversas'] = []
            request.session.modified = True
            return render(request, 'index.html', {'form': PerguntaForm(), 'conversas': request.session['conversas']})

        form = PerguntaForm(request.POST)
        if form.is_valid():
            pergunta = form.cleaned_data['pergunta']
            # Adiciona o texto pré-definido à pergunta do usuário
            prompt = texto_pre_definido + pergunta + "Translate to Portuguese"
            try:
                # Utiliza o modelo para gerar a resposta
                response = model.generate_content(prompt)
                if response and response.text:
                    resposta = json.loads(response.text)
                else:
                    resposta = "Desculpe, não consegui gerar uma resposta."
            except Exception as e:
                resposta = f"Erro ao gerar resposta: {str(e)}"
            
            # Armazena a pergunta e a resposta no histórico de conversas
            request.session['conversas'].append({'pergunta': pergunta, 'resposta': resposta})
            request.session.modified = True
    else:
        form = PerguntaForm()

    return render(request, 'index.html', {'form': form, 'conversas': request.session['conversas']})
