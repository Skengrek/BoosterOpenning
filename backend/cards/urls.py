from django.urls import path
from cards import views

# define the urls
urlpatterns = [
    path("lists/", views.cardsListing),
    path("lists/<int:pk>/", views.cardDetails),
    path("booster/open/", views.random_booster),
]
