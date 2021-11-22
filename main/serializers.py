from rest_framework import serializers
from main.models import Job, Category, BoardUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class BoardUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardUser
        fields = ('id', 'username', 'first_name', 'last_name')


class JobSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    created_by = BoardUserSerializer(read_only=True)

    class Meta:
        model = Job
        fields = ('name', 'category', 'description', 'responsibility', 'qualifications', 'benefits', 'published_date',
                  'positions_number', 'salary_from', 'salary_to', 'location', 'job_nature', 'created_by')
