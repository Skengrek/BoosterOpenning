from users.models import User
from cards.models import Set
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import UserSerializer, UserCreateSerializer


def usersListView(request):

    if request.method == "GET":
        # List all User
        lists = User.objects.all()
        serializer = UserSerializer(lists, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def userCreateView(request):
    if request.method == "POST":
        # Add a User
        data = JSONParser().parse(request)
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def userDetails(request, pk):
    try:
        _list = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = UserSerializer(_list, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.error, status=400)

    elif request.method == "DELETE":
        # delete the task
        _list.delete()
        # return a no content response.
        return HttpResponse(status=204)

    elif request.method == "GET":
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)
    

class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        serializer = self.get_serializer(data=request.data)
        # Check if the data is valid
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Access the validated user from the serializer
        user = serializer.user
        now = timezone.now()
        last_login = user.last_login
        if last_login is None or last_login.date() < now.date():
            last_set = Set.objects.latest("release_date")
            last_set.add_booster_to_user(user, 5)
        user.last_login = now
        user.save()
        
        # Return the original response or modify it as needed
        return response