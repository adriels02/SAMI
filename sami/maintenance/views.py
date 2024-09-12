from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DocumentForm
from django.urls import reverse
from django.contrib.auth import logout
from .models import Document
from PyPDF2 import PdfReader
from io import BytesIO
from langchain_openai import OpenAI
import requests
import os


@login_required(login_url='/management/login')
def home(request):
    context = {}
    return render(request, "maintenance/home.html", context)

def logout_view(request): 
    logout(request)
    return redirect(reverse('management:logar'))

@login_required(login_url='/management/login')
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.enviado_por = request.user
            document.save()
            messages.success(request, 'Arquivo enviado com sucesso!')
            return redirect('maintenance:upload_document')
    else:
        form = DocumentForm()
    return render(request, 'maintenance/upload_document.html', {'form': form})

@login_required(login_url='/management/login')
def list_documents(request):
    documents = Document.objects.all()
    return render(request, 'maintenance/list_documents.html', {'documents': documents})

@login_required(login_url='/management/login')
def q_and_a(request):
    documents = Document.objects.all()
    responses = ''

    if request.method == 'POST':
        document_id = request.POST.get('document_id')
        query = request.POST.get('query') 
        
        if document_id and query:
            document = get_object_or_404(Document, id=document_id)
            pdf_text = extract_text(document)
            query += " Responda apenas com base no texto que segue e em português. Se a pergunta não tiver relação com o texto, avise que não tem relação. Texto (em português):" 
            query += pdf_text
            responses = consult_llm(query) 
        else:
            messages.error(request, "Por favor, selecione um documento e insira uma pergunta.")

    return render(request, 'maintenance/q_and_a.html', {'documents': documents, 'responses': responses})

def consult_llm(query):
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    llm = OpenAI()
    
    response = llm.invoke(query) 
    return response
   

def extract_text(document, max_tokens=3500):
    with document.arquivo.open('rb') as pdf_file:
        pdf_bytes = BytesIO(pdf_file.read())
    content = PdfReader(pdf_bytes)        
    full_text = ""
    for page in content.pages:
        if len(full_text.split()) < max_tokens:
            full_text += page.extract_text()
        else:
            break
    return full_text[:max_tokens]
