from django.conf.urls import url
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib import admin

from server import settings
from tournaments import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^accounts/signup/$', views.signup, name='signup'),
    url(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('tournaments/<int:pk>/singup/', views.tournament_signup, name='tournament_signup'),
    path('tournaments/<int:pk>/', views.TournamentDetailView.as_view(), name='tournament_detail'),
    path('tournaments/', views.TournamentListView.as_view(), name='tournament_list'),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
