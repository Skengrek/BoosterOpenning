from django.contrib import admin
from cards.models import Card, Set, Booster
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import admin
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from cards.forms import AskForExtension
from cards.tasks import import_set_task
from celery.result import AsyncResult
from django.http import JsonResponse
from logging import getLogger

logger = getLogger(__name__)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("name", "rarity", "extension_id")


@admin.register(Booster)
class BoosterAdmin(admin.ModelAdmin):
    list_display = ("user", "get_set_id", "number")

    def get_set_id(self, obj):
        return obj.set.extension_id
    
    get_set_id.admin_order_field  = 'set'  #Allows column order sorting
    get_set_id.short_description = 'Extension ID'  #Renames column head

@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ("name", "series", "extension_id")
    change_list_template = 'admin/import_data_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-set/', self.admin_site.admin_view(self.start_import), name='import_set'),
            path('import-progress/<task_id>/', self.admin_site.admin_view(self.import_progress), name='import_progress'),
        ]
        return custom_urls + urls

    def start_import(self, request):
        if request.method == 'POST':
            form = AskForExtension(request.POST)
            if form.is_valid():
                set_id = form.cleaned_data['set_id']
                # Trigger the Celery task
                task = import_set_task.delay(set_id)
                # Redirect to a progress page, passing the task ID
                return redirect(reverse('admin:import_progress', kwargs={'task_id': task.id}))
        else:
            form = AskForExtension()

        context = {'form': form, 'title': 'Start Data Import'}
        return render(request, 'admin/import_set.html', context)

    def import_progress(self, request, task_id):
        # Similar to the import_progress view outside admin
        task = AsyncResult(task_id)
        if task.state == 'PROGRESS':
            response = {
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 1)
            }
        elif task.state == 'SUCCESS':
            response = {'state': task.state, 'data': task.result.get('data')}
        else:
            response = {'state': task.state}
        return JsonResponse(response)
    
    # Optionally, add a button on the changelist page for the import task
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['import_button'] = True
        return super().changelist_view(request, extra_context=extra_context)
    

class YourModelAdmin(admin.ModelAdmin):
    def response_change(self, request, obj):
        if "_start_import" in request.POST:
            # Trigger the import from the model's change view
            task = import_set_task.delay(obj.some_field)
            return HttpResponseRedirect(reverse('admin:import_progress', args=[task.id]))
        return super().response_change(request, obj)

    def get_changeform_buttons(self, request, obj=None):
        if obj:
            return [{
                'url': reverse('admin:start_import'),
                'label': 'Start Import',
                'class': 'button',
            }]
        return []
