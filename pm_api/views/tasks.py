from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from pm_api.models import Project, Task
from pm_api.serializers import  TaskSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication


@extend_schema(tags=['Tasks'])
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

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
