from django.urls import path
from .views import *

urlpatterns = [
    path('signup', customer_signup, name="signup"),
    path('login', customer_login, name="login"),
    path('logout', customer_logout, name="logout"),
    path('dashboard', customer_dashboard, name="dashboard"),
    path('compute_calorie', customer_calorie_compute, name="compute_calories"),

]
