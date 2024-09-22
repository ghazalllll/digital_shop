from django.urls import path
from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]





# from django.urls import path
# from .views import RegisterView
# Ourlpatterns = [
# path('register/', RegisterView.as_view())]