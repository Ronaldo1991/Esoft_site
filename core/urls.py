from django.urls import path, include, re_path

from django.views.generic.base import RedirectView
from core.views import IndexView, HomeView, ProdutoView
from core.views import Login, Logout, DadosJSONView
from .views import AcountRegister


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register', AcountRegister.as_view(), name='register'),
    # re_path(r'^login/register$', RedirectView.as_view(url='http://127.0.0.1:8000/register', permanent=False), name='register'),
    path('home', HomeView.as_view(), name='home'),
    path('produtos', ProdutoView.as_view(), name='produtos'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    # re_path(r'^logout/register$', RedirectView.as_view(url='http://127.0.0.1:8000/register', permanent=False), name='logout'),
    path('dados/', DadosJSONView.as_view(), name='dados'),
    
]