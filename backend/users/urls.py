from django.urls import path
from users import views

# define the urls
urlpatterns = [
    path("lists/", views.usersView, name="users-list"),
    path("profile/<int:pk>", views.userDetails, name="user-pk"),

]
