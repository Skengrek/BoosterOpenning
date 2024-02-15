from django.urls import path
from users import views

# define the urls
urlpatterns = [
    path("", views.usersListView, name="users-list"),
    path("create/", views.userCreateView, name="users-create"),
    path("profile/<int:pk>", views.userDetails, name="user-pk"),
]
