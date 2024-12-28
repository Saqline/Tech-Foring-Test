from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from pm_api.models import  Task, Comment
from pm_api.serializers import  CommentSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication


@extend_schema(tags=['Comments'])
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

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