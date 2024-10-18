from django.urls import path
from cards.views.cards import *

# define the urls
urlpatterns = [
    path("lists/", CardListing.as_view()),
    path("lists/<int:pk>/", CardDetails.as_view()),
    path("booster/open/", RandomBooster.as_view()),
    path("booster/user/list/boosters", ListUserBoosters.as_view()),
    path("booster/user/list/cards", ListUserCards.as_view()),
    path("booster/user/open/<str:extension_id>", OpenBooster.as_view()),
    path("example/<int:number_of_cards>", GetCardsExample.as_view()),
]
