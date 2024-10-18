from django.shortcuts import render, redirect
from django.urls import reverse
from cards.forms import DataImportForm
from cards.tasks import import_set_task  # assuming we use Celery for async task
from celery.result import AsyncResult
from django.http import JsonResponse

def start_import(request):
    if request.method == 'POST':
        form = DataImportForm(request.POST)
        if form.is_valid():
            set_id = form.cleaned_data['set_id']
            # Trigger the Celery task for the import
            task = import_set_task.delay(set_id)
            # Redirect to a progress page, passing the task ID
            return redirect(reverse('import_progress', kwargs={'task_id': task.id}))
    else:
        form = DataImportForm()

    return render(request, 'import_set.html', {'form': form})


def import_progress(request, task_id):
    task = AsyncResult(task_id)
    if task.state == 'PROGRESS':
        response = {'state': task.state, 'current': task.info.get('current', 0), 'total': task.info.get('total', 1)}
    elif task.state == 'SUCCESS':
        response = {'state': task.state, 'data': task.result.get('data')}
    else:
        response = {'state': task.state}
    return JsonResponse(response)