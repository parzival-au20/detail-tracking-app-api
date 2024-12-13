"""
URL mappings for to-do API
"""


from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter
from todo.views import ToDoViewSet

app_name = 'todo'


# Main router
router = SimpleRouter()
router.register(r'users', ToDoViewSet, basename='users')

# Nested router for posts
todos_router = NestedSimpleRouter(router, r'users', lookup='user')
todos_router.register(r'todos', ToDoViewSet, basename='user-todos')

urlpatterns = router.urls + todos_router.urls
