from django.urls import path
from cards import views

# define the urls
urlpatterns = [
    path("lists/", views.CardListing.as_view()),
    path("lists/<int:pk>/", views.CardDetails.as_view()),
    path("booster/open/", views.RandomBooster.as_view()),
]
