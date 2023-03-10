import ccxt
import time
import requests
import random
from bs4 import BeautifulSoup

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.cache import cache

from .forms import UserRegisterForm, CommentForm, ContactForm
from .models import Blog, Article, Comment, UserVote,CardDeck


# Create your views here.

def card_deck_52(request):
    card_deck = list(CardDeck.objects.all())
    print(card_deck)
    random.shuffle(card_deck)
    context = {'card_deck': card_deck}
    return render(request, 'blog/cards_52.html', context=context)



def get_news():
    url = 'https://cryptonews.net/ru/news/bitcoin/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('a', class_='title')
    name_title = title.text

    img = soup.find('span', class_='image lazy')
    foto = img.get('data-src')
    news_url = 'https://cryptonews.net' + title['href']

    news_response = requests.get(news_url,headers=headers)
    news_soup = BeautifulSoup(news_response.text,'html.parser')
    news_text = news_soup.find('div',class_='news-item detail content_text')
    p_tags = news_text.find_all('p')
    p_texts = [p_tag.text for p_tag in p_tags]
    text = ''
    for elem in p_texts:
        text = text + elem + ' '
    context = {'name_title': name_title,'foto':foto,'text':text}
    return context


def get_btc_exchange_rate():
    cache_key = 'btc_exchange_rate'
    exchange = ccxt.binance()
    symbol = 'BTC/USDT'
    timeframe = '1d'
    limit = 2

    end_time = int(time.time() * 1000)
    start_time = end_time - (limit * 24 * 60 * 60 * 1000)

    # Извлекаем данные из кэша
    cached_data = cache.get(cache_key)
    if cached_data:
        context = cached_data
    else:
        # Если данные не найдены в кэше, выполняем запрос к API Binance
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit, since=start_time)
        context = {'close': round(ohlcv[0][-2])}
        # Сохраняем данные в кэше
        cache.set(cache_key, context, timeout=60)  # timeout - время жизни кэша в секундах

    return context


def last_add_article():
    latest_article = Article.objects.latest('date')
    title = latest_article.title
    image = latest_article.photo
    pk = latest_article.pk
    context = {'title': title, 'image': image, 'pk': pk, }
    return context


def home(request):
    context_1 = last_add_article()
    context_2 = get_btc_exchange_rate()
    context_3 = get_news()
    context = {**context_1, **context_2, **context_3}
    return render(request, 'blog/home.html', context=context)


def market_view(request):
    obj = Blog.objects.all()
    context = {
        'obj': obj,
    }
    return render(request, 'blog/market_view.html', context=context)


def articles_list(request):
    obj = Article.objects.all()

    context = {
        'obj': obj,
    }
    return render(request, 'blog/articles.html', context=context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('contact')
    else:
        form = ContactForm()
        form.fields['full_name'].label = "имя"
        form.fields['email'].label = "почта"
        form.fields['subject'].label = "тема"
        form.fields['message'].label = "сообщение"
        return render(request, 'blog/contact.html', {'form': form})


def article_detail(request, pk):
    article = Article.objects.get(id=pk)
    comments = article.comments.all()
    form = CommentForm()
    form.fields['text'].label = ''
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', pk=article.pk)
    return render(request, 'blog/article_detail.html', {'article': article, 'comments': comments, 'form': form})


def positive_post(request, pk):
    # grab the post and the user
    article = Article.objects.get(pk=pk)
    user = request.user
    # Now try to find if that user has voted
    try:
        voted = UserVote.objects.get(article=article, user=user)
        # if you can then, user already voted.
        return HttpResponse("YOU ALREADY VOTED")
    except:
        # If u can not, the user didnt vote yet, so
        # create a new obejct.
        obj = UserVote()
        obj.article = article
        obj.user = user
        obj.vote_type = "positive"
        obj.save()
        # add positive vote to post DB
        article.post_pos += 1
        article.save()
        return redirect('article_detail', pk=article.pk)


def negative_post(request, pk):
    # grab the post and the user
    article = Article.objects.get(pk=pk)
    user = request.user
    # Now try to find if that user has voted
    try:
        voted = UserVote.objects.get(article=article, user=user)
        # if you can then, user already voted.
        return HttpResponse("YOU ALREADY VOTED")
    except:
        # If u can not, the user didnt vote yet, so
        # create a new obejct.
        obj = UserVote()
        obj.article = article
        obj.user = user
        obj.vote_type = "positive"
        obj.save()
        # add positive vote to post DB
        article.post_pos += 1
        article.save()
        return redirect('article_detail', pk=article.pk)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('articles')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('articles')
    else:

        form = AuthenticationForm()
        form.fields["username"].widget.attrs["autocomplete"] = "off"
        form.fields["password"].widget.attrs["autocomplete"] = "off"
        form.fields['username'].label = "логин"
        form.fields['password'].label = "пароль"

    return render(request, 'blog/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


