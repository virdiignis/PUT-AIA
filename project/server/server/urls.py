from django.conf.urls import url
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import path, include
from django.contrib import admin

from server import settings
from tournaments import views

urlpatterns = [
    path('', views.TournamentListView.as_view(), name='tournament_list'),
    url(r'^accounts/signup/$', views.signup, name='signup'),
    url(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('tournaments/new/', views.tournament_new, name='tournament_new'),
    path('tournaments/<int:id>/edit/', views.tournament_edit, name='tournament_edit'),
    path('tournaments/<int:id>/add_sponsor/', views.tournament_add_sponsor, name='tournament_add_sponsor'),
    path('tournaments/<int:pk>/singup/', views.tournament_signup, name='tournament_signup'),
    path('tournaments/<int:pk>/', views.TournamentDetailView.as_view(), name='tournament_details'),
    path('encounters/<int:pk>/', views.EncounterDetailView.as_view(), name='encounter'),
    path('encounters/<int:pk>/winner/<int:winner>/', views.encounter_set_winner, name='winner'),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
