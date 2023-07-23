from django.urls import path
from . import views

urlpatterns = [
    path(' ', views.home, name='home'),
    path('views/', views.market_view, name='market_view'),
    path('articles/', views.articles_list, name='articles'),
    path('contact/', views.contact, name='contact'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('<int:pk>/up/',views.positive_post, name='positive_post'),
    path('<int:pk>/down/',views.negative_post, name='negative_post'),
    path('card_deck_52/', views.card_deck_52, name='card_deck_52'),

]
