from django.shortcuts import render
from .models import Topic
from django.http import HttpRequest, HttpResponseRedirect
from .forms import TopicForm, EntryForm
from django.urls import reverse

def index(request: HttpRequest):
    '''Página principal do Learning_log'''
    return render(request, 'learning_logs/index.html')

def topics(request: HttpRequest):
    '''Mostra todos os assuntos'''
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}

    return render(request, 'learning_logs/topics.html', context)

def topic(request: HttpRequest, topic_id):
    '''Mostra um único assunto e todas as suas entradas'''
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}

    return render(request, 'learning_logs/topic.html', context)


def new_topic(request: HttpRequest):
    '''Adiciona um novo assunto'''
    if request.method != 'POST':
        # Nenhum dado submetido; cria um formulário em branco
        form = TopicForm()
    else:
        # Dados de POST submetidos; processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topics')) #Esse reverse pega o name que você definiu no arquivo urls
        
    context = {'form': form}

    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request: HttpRequest, topic_id):
    '''Acrescenta uma nova anotação para um assunto'''
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # Nenhuma dado submetido; cria um formulário em branco
        form = EntryForm()
    else:
        # Dados de POST submetidos; processa os dados
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False) # Cria um novo objeto mas não salva no BD
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic'), args=[topic_id])
    
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)
