from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pm_api.views.users import UserViewSet
from pm_api.views.comments import CommentViewSet
from pm_api.views.projects import ProjectViewSet
from pm_api.views.tasks import TaskViewSet



router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'comments', CommentViewSet, basename='comment')

# URL Patterns
urlpatterns = [
    path('api/', include(router.urls)),  
    path('projects/<int:project_id>/tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-tasks'),
    path('tasks/<int:task_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-comments'),
  
]
