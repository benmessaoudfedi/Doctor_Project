from django.contrib import admin
from django.urls import path
from Doctor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),
    path('home/', views.home, name="home"),
    path('', views.accueil, name="accueil"),

]
