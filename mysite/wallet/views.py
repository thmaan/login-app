from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.
def home(request):
	return render(request, 'wallet/home.html')

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/task-list/',
		'Detail View':'/task-detail/<str:pk/',
		'Create':'/task-create/',
		'Update':'task-update/<str:pk>/',
		'Delete':'task-delete/<str:pk>/',
		}
	render(request, 'wallet/home.html')
	return Response(api_urls)

@api_view(['GET'])
def taskList(request):
	task = Task.objects.all()
	serializer = TaskSerializer(task, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
	task = Task.objects.get(id=pk)
	serializer = TaskSerializer(task, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def taskCreate(request):
	serializer = TaskSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def taskUpdate(request, pk):
	task = Task.objects.get(id=pk)
	serializer = TaskSerializer(instance=task ,data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['DELETE'])
def taskDelete(request, pk):
	task = Task.objects.get(id=pk)
	task.delete()

	return Response("Item deleted!")