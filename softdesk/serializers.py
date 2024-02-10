from rest_framework import serializers
from accounts.models import User

from accounts.serializers import UserSerializer
from softdesk.models import Issue, Project, ProjectContributor, Comment


class ContributorSerializer(serializers.ModelSerializer):
    contributor = UserSerializer(source='contributor.contributor', read_only=True)
    class Meta:
        model = ProjectContributor
        fields = ['contributor', 'project']


class AddContributorSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Contributor username")

class RemoveContributorSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Contributor username")


class ProjectListSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    def get_creator(self, instance):
        return instance.creator.username

    class Meta:
        model = Project
        fields = '__all__'


class ProjectDetailSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    contributors = serializers.SerializerMethodField()

    def get_creator(self, instance):
        return instance.creator.username

    def get_contributors(self, instance):
        contributors = ProjectContributor.objects.filter(project=instance)
        return [contributor.contributor.username for contributor in contributors]

    class Meta:
        model = Project
        fields = ['id', 'name', 'project_type', 'creator', 'created_at', 'description', 'contributors']


class ProjectSerializer(serializers.ModelSerializer):
    # To create new Project
    class Meta:
        model = Project
        fields = ['name', 'description', 'project_type']


class IssueListSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(source='creator.username', read_only=True)
    assigned_to = serializers.SerializerMethodField()

    def get_creator(self, instance):
        return instance.creator.username
    
    def get_assigned_to(self, instance):
        return instance.assigned_to.username
    
    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'creator', 'assigned_to', 'status', 'priority', 'tag', 'created_at']


class IssueSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(source='creator.username', read_only=True)
    assigned_to = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Issue
        fields = ['id', 'name', 'description', 'creator', 'assigned_to', 'status', 'priority', 'tag', 'created_at']

    def get_creator(self, instance):
        return instance.creator.username
    

class CommentSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(source='creator.username', read_only=True)
    def get_creator(self, instance):
        return instance.creator.username
    
    class Meta:
        model = Comment
        fields = ['id', 'creator', 'comment', 'created_at']
