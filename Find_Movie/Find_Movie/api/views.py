import os
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from Find_Movie.api.serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse
import subprocess
from django.conf import settings
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from .models import SavedMovie
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import update_session_auth_hash


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        # Update session to prevent logout after password change
        update_session_auth_hash(request, user)

        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        profile_picture = request.FILES.get('profile_picture')

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        # Provera i upload nove slike
        if profile_picture:
            # Kreiranje putanje za čuvanje slike kao 'username.png'
            file_name = f'profile_pics/{user.username}.png'
            old_path = os.path.join(settings.MEDIA_ROOT, file_name)
            if os.path.exists(old_path):
                os.remove(old_path)
            file_path = default_storage.save(
                file_name, ContentFile(profile_picture.read()))
            user.profile_picture = file_path

        user.save()  # Čuvanje izmena

        # Koristi default_storage.url() za generisanje URL-a slike
        profile_picture_url = default_storage.url(
            user.profile_picture) if user.profile_picture else None

        return Response({
            'message': 'User updated successfully',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_picture': profile_picture_url,
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user_profile(request):
    user = request.user
    if request.user.is_authenticated:
        # Definiši putanju do slike
        profile_pic_url = None
        profile_pic_path = f'profile_pics/{user.username}.png'

        # Proveri da li fajl postoji
        if default_storage.exists(profile_pic_path):
            profile_pic_url = f'http://localhost:8000/api{settings.MEDIA_URL}{profile_pic_path}'

        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_picture': profile_pic_url  # Vraćaj URL slike ako postoji
        })
    return Response({'error': 'User not authenticated'}, status=401)


@api_view(['GET'])
def get_saved_movies(request):
    if request.user.is_authenticated:
        user = request.user
        saved_movies = SavedMovie.objects.filter(user=user)

        # Formira listu sačuvanih filmova sa relevantnim informacijama
        movies_list = [{'movie_id': movie.movie_id,
                        'saved_at': movie.saved_at} for movie in saved_movies]

        return Response(movies_list, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Morate biti prijavljeni da biste videli sačuvane filmove.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def toggle_save_movie(request):
    if request.user.is_authenticated:
        user = request.user
        movie_id = request.data.get('movie_id')

        # Proverite da li je film već sačuvan
        saved_movie = SavedMovie.objects.filter(
            user=user, movie_id=movie_id).first()

        if saved_movie:
            # Ako je film sačuvan, uklonite ga
            saved_movie.delete()
            return Response({'message': 'Film je uklonjen iz sačuvanih filmova.'}, status=status.HTTP_200_OK)
        else:
            # Ako film nije sačuvan, dodajte ga
            new_saved_movie = SavedMovie(user=user, movie_id=movie_id)
            new_saved_movie.save()
            return Response({'message': 'Film je sačuvan.'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Morate biti prijavljeni da biste sačuvali ili uklonili film.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def is_movie_saved(request, movie_id):
    if request.user.is_authenticated:
        user = request.user
        # Proveri da li je film sačuvan za datog korisnika
        saved_movie = SavedMovie.objects.filter(
            user=user, movie_id=movie_id).first()
        if saved_movie:
            return Response({'is_saved': True}, status=status.HTTP_200_OK)
        else:
            return Response({'is_saved': False}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Morate biti prijavljeni.'}, status=status.HTTP_401_UNAUTHORIZED)


# Registration View


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username, password=password, email=email)
        user.save()

        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

# Login View


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Logout View


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# User Info View


class UserView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return Response({
                'username': user.username,
                'email': user.email
            })
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication,]
    # permission_classes = [IsAuthenticated,]


def run_proxy_script(request):
    """Run the proxy script and return the selected proxy."""
    try:
        # Pokrećemo skriptu i hvatamo njen izlaz
        script_path = os.path.join(
            'C:\\Users\\mihaj\\source\\Find_Movie\\scrapping\\proxy.py')

        result = subprocess.run(['python', script_path],
                                capture_output=True, text=True)

        # Proveravamo da li je izvršenje bilo uspešno
        if result.returncode == 0:
            # Pretpostavljamo da skripta ispisuje korišćeni proxy u stdout
            selected_proxy = result.stdout.strip()  # Uklanjamo prazne prostore
            return JsonResponse({'status': 'success', 'output': selected_proxy})
        else:
            # Ako je došlo do greške u izvršavanju skripte
            return JsonResponse({'status': 'error', 'message': result.stderr})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def get_html_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'torrents', filename)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return HttpResponse(file.read(), content_type='text/html')
    else:
        raise Http404("File does not exist")


def get_subtitles_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'subtitles', filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return HttpResponse(file.read(), content_type='text/html')
    else:
        raise Http404("File does not exist")


def run_torrent_script(request, movie_title):
    # Pokrenite skriptu sa nazivom filma
    try:
        script_path = os.path.join(
            'C:\\Users\\mihaj\\source\\Find_Movie\\scrapping\\torrent.py')

        result = subprocess.run(['python', script_path, movie_title],
                                check=True, capture_output=True, text=True)
        return JsonResponse({'message': 'Script executed successfully', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': 'Failed to execute script', 'details': str(e)}, status=500)


def run_subtitle_script(request, movie_title):
    # Pokrenite skriptu sa nazivom filma
    try:
        script_path = os.path.join(
            'C:\\Users\\mihaj\\source\\Find_Movie\\scrapping\\subtitles.py')

        result = subprocess.run(['python', script_path, movie_title],
                                check=True, capture_output=True, text=True)
        return JsonResponse({'message': 'Script executed successfully', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': 'Failed to execute script', 'details': str(e)}, status=500)
