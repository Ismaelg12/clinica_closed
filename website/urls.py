from django.urls import path
from website import views

urlpatterns = [
	path('',views.home,name="site"),
	# path('sucesso',views.success,name="sucesso")
]