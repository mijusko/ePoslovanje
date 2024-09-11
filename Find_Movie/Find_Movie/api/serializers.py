from django.contrib.auth.models import User
from rest_framework import serializers
from .models import SavedMovie


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password',
                  'first_name', 'last_name', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class SavedMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedMovie
        fields = ['user', 'movie_id', 'saved_at']
