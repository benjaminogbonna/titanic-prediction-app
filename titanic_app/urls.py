from django.urls import path
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
app_name = 'titanic_app'

urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.IndexView.as_view(), name='index'),
]
# urlpatterns += staticfiles_urlpatterns()
