from rest_framework import serializers  # Importing serializers module from rest_framework
from accounts.models import User  # Importing User model from accounts app
from accounts.serializers import UserSerializer  # Importing UserSerializer from accounts.serializers module
from softdesk.models import Issue, Project, ProjectContributor, Comment  # Importing models from softdesk app

# Serializer for ProjectContributor model
class ContributorSerializer(serializers.ModelSerializer):
    contributor = UserSerializer(source='contributor.contributor', read_only=True)  # Serializer for the contributor user
    class Meta:
        model = ProjectContributor  # Setting the model to ProjectContributor
        fields = ['contributor', 'project']  # Specifying the fields to include in the serialized representation

# Serializer for adding a contributor to a project
class AddContributorSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Contributor username")  # Field for the username of the contributor to be added

# Serializer for removing a contributor from a project
class RemoveContributorSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Contributor username")  # Field for the username of the contributor to be removed

# Serializer for listing projects
class ProjectListSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()  # Serializer method field for the creator's username

    def get_creator(self, instance):
        return instance.creator.username  # Method to get the username of the project creator

    class Meta:
        model = Project  # Setting the model to Project
        fields = '__all__'  # Specifying to include all fields in the serialized representation

# Serializer for project details
class ProjectDetailSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()  # Serializer method field for the creator's username
    contributors = serializers.SerializerMethodField()  # Serializer method field for the contributors' usernames

    def get_creator(self, instance):
        return instance.creator.username  # Method to get the username of the project creator

    def get_contributors(self, instance):
        contributors = ProjectContributor.objects.filter(project=instance)  # Getting contributors associated with the project
        return [contributor.contributor.username for contributor in contributors]  # Returning usernames of contributors

    class Meta:
        model = Project  # Setting the model to Project
        fields = ['id', 'name', 'project_type', 'creator', 'created_at', 'description', 'contributors']  # Specifying fields to include in the serialized representation

# Serializer for creating a new project
class ProjectSerializer(serializers.ModelSerializer):
    # To create new Project
    class Meta:
        model = Project  # Setting the model to Project
        fields = ['name', 'description', 'project_type']  # Specifying fields to include in the serialized representation

# Serializer for listing issues
class IssueListSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(source='creator.username', read_only=True)  # Field for the username of the issue creator
    assigned_to = serializers.SerializerMethodField()  # Serializer method field for the assigned user's username

    def get_creator(self, instance):
        return instance.creator.username  # Method to get the username of the issue creator
    
    def get_assigned_to(self, instance):
        return instance.assigned_to.username  # Method to get the username of the assigned user
    
    class Meta:
        model = Issue  # Setting the model to Issue
        fields = ['id', 'name', 'description', 'creator', 'assigned_to', 'status', 'priority', 'tag', 'created_at']  # Specifying fields to include in the serialized representation

# Serializer for issue details
class IssueSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(source='creator.username', read_only=True)  # Field for the username of the issue creator
    assigned_to = serializers.CharField(allow_blank=True, required=False)  # Field for the username of the assigned user

    class Meta:
        model = Issue  # Setting the model to Issue
        fields = ['id', 'name', 'description', 'creator', 'assigned_to', 'status', 'priority', 'tag', 'created_at']  # Specifying fields to include in the serialized representation

    def get_creator(self, instance):
        return instance.creator.username  # Method to get the username of the issue creator

# Serializer for comments
class CommentSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(source='creator.username', read_only=True)  # Field for the username of the comment creator
    def get_creator(self, instance):
        return instance.creator.username  # Method to get the username of the comment creator
    
    class Meta:
        model = Comment  # Setting the model to Comment
        fields = ['id', 'creator', 'comment', 'created_at']  # Specifying fields to include in the serialized representation
