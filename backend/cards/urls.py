from django.urls import path
from cards import views

# define the urls
urlpatterns = [
    path("lists/", views.CardListing.as_view()),
    path("lists/<int:pk>/", views.CardDetails.as_view()),
    path("booster/open/", views.RandomBooster.as_view()),
    path("booster/user/list/boosters", views.ListUserBoosters.as_view()),
    path("booster/user/list/cards", views.ListUserCards.as_view()),
    path("booster/user/open/<str:extension_id>", views.OpenBooster.as_view()),
    path("example/<int:number_of_cards>", views.GetCardsExample.as_view()),
]
