from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DocumentForm
from django.urls import reverse
from django.contrib.auth import logout
from .models import Document
import PyPDF2
from langchain_openai import OpenAI
from langchain.text_splitter import CharacterTextSplitter
import openai
from langchain_openai import OpenAIEmbeddings
import os
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

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
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()
    messages.success(request, 'Arquivo deletado com sucesso!')
    return redirect('maintenance:list_documents')

@login_required(login_url='/management/login')
def q_and_a(request):
    responses = ''
    documents = Document.objects.all()
    if request.method == 'POST':
        query = request.POST.get('query') 
        
        if  query:
            
            pdf_index = ChoosePdf(query)
            try:
                pdf_index = int(pdf_index)
            except ValueError:
                return render(request, 'maintenance/q_and_a.html', {'responses': pdf_index})
            
            vector_store = extract_text(pdf_index)
            responses = consult_llm(query, vector_store) 
        else:
            messages.error(request, "Por favor, selecione um documento e insira uma pergunta.")

    return render(request, 'maintenance/q_and_a.html', {'documents': documents, 'responses': responses})

def select_q_and_a(request):
    documents = Document.objects.all()
    responses = ''

    if request.method == 'POST':
        document_id = request.POST.get('document_id')
        query = request.POST.get('query') 
        print(document_id)
        if  query and document_id:
            document_id = int(document_id)
            document_id = document_id - 1
            vector_store = extract_text(document_id)
            responses = consult_llm(query, vector_store) 

        else:
            messages.error(request, "Por favor, selecione um documento e insira uma pergunta.")

    return render(request, 'maintenance/select_q_and_a.html', {'documents': documents, 'responses': responses})





def consult_llm(query, vector_store):
   
    llm = OpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages= True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vector_store.as_retriever(),
        memory = memory
    )
    response = conversation_chain.run(query)
    return response
   

def extract_text(pdf_index):
   
    text = load_document(pdf_index)
        
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size = 1500,
        chunk_overlap = 300,
        length_function = len
    )
    chunks = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings(openai_api_key="OPENAI_API_KEY")    
    vector_store = FAISS.from_texts(texts = chunks, embedding = embeddings)
    

    return vector_store


def load_document(pdf_index):

    documents = Document.objects.all()
    target_pdf = documents[pdf_index]

    pdf_file = target_pdf.arquivo  
    with pdf_file.open('rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        
       
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    
  
    return text  

def ChoosePdf(query):

    titles = []

    for document in Document.objects.all():
        titles.append(document.titulo)

   
    llm = OpenAI()

    indexPdf = llm.invoke(input=f"Seu papel é identificar qual título a pergunta se refere, caso identifique qual, informe apenas um número que represente a posição da lista desse título que foi identificado, considerando que a primeira posição da lista é 0. se não conseguir indentificar escreva para o usuário informando para ele acrescentar o manual que ele está se referindo na pergunta. Pergunta: {query} Títulos: {titles}")
    
    return indexPdf