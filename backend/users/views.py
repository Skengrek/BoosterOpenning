from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


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