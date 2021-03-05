from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from django.conf.urls import url

urlpatterns = [
                  path('signup', customer_signup, name="signup"),
                  path('login', customer_login, name="login"),
                  path('logout', customer_logout, name="logout"),
                  path('dashboard', customer_dashboard, name="dashboard"),
                  path('compute_calorie', customer_calorie_compute, name="compute_calories"),
                  path('view_calorie_submission', customer_calorie_view, name="view_calorie_submission"),
                  # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                  #     activate, name='activate'),
                  path('activate/<slug:uidb64>/<slug:token>/',activate, name='activate')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
