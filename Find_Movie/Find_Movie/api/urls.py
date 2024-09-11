from django.urls import path, include
from rest_framework import routers
from Find_Movie.api import views
from rest_framework.authtoken.views import ObtainAuthToken
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import path

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', ObtainAuthToken.as_view()),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user/', views.UserView.as_view(), name='user'),
    path('run-proxy/', views.run_proxy_script, name='run_proxy'),
    path('get-html/<str:filename>/', views.get_html_file, name='get_html_file'),
    path('get-subtitle/<str:filename>/',
         views.get_subtitles_file, name='get_subtitle_file'),
    path('run-torrent-script/<str:movie_title>/',
         views.run_torrent_script, name='run_torrent_script'),
    path('run-subtitle-script/<str:movie_title>/',
         views.run_subtitle_script, name='run_subtitle_script'),
    path('toggle_save_movie/', views.toggle_save_movie, name='toggle_save_movie'),
    path('is_movie_saved/<int:movie_id>/',
         views.is_movie_saved, name='is_movie_saved'),
    path('saved_movies/', views.get_saved_movies, name='get_saved_movies'),
    path('user-profile/', views.get_user_profile, name='get_user_profile'),
    path('user/update/', views.UpdateUserView.as_view(), name='user-update'),
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change_password'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
