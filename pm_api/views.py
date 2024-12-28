from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Project, ProjectMember, Task, Comment
from .serializers import UserSerializer, ProjectSerializer, ProjectMemberSerializer, TaskSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication


@extend_schema(tags=['Users'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=request.data['password']
        )
        return Response(UserSerializer(user).data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        user = User.objects.filter(username=request.data['username']).first()
        if user and user.check_password(request.data['password']):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=400)

@extend_schema(tags=['Projects'])
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

@extend_schema(tags=['Tasks'])
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        if project_id:
            return Task.objects.filter(project_id=project_id)
        return Task.objects.all()

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)
        
    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses=TaskSerializer,
        methods=['GET', 'POST']
    )
    @action(detail=False, methods=['get', 'post'], url_path='projects/(?P<project_id>[^/.]+)/tasks')
    def project_tasks(self, request, project_id=None):
        if request.method == 'GET':
            return self.list(request)
        elif request.method == 'POST':
            return self.create(request)


@extend_schema(tags=['Comments'])
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        if task_id:
            return Comment.objects.filter(task_id=task_id)
        return Comment.objects.all()

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)
        serializer.save(task=task)

    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses=CommentSerializer,
        methods=['GET', 'POST']
    )
    @action(detail=False, methods=['get', 'post'], url_path='tasks/(?P<task_id>[^/.]+)/comments')
    def task_comments(self, request, task_id=None):
        if request.method == 'GET':
            return self.list(request)
        elif request.method == 'POST':
            return self.create(request)