from django.urls import include, path
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _

from wagtail.core import hooks
from wagtail.contrib.modeladmin.views import CreateView, EditView
from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register, ModelAdminGroup)

from .models import EventDirectory, EventDirectoryFile
from .button_helper import EventDirectoryHelper
from .views import validate, import_file


class EventDirectoryEditView(EditView):

    def form_valid(self, form):
        self.object = form.save_all(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

class EventDirectoryCreateView(CreateView):

    def form_valid(self, form):
        self.object = form.save_all(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class EventDirectoryFileCreateView(CreateView):

    def form_valid(self, form):
        self.object = form.save_all(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class EventDirectoryAdmin(ModelAdmin):
    model = EventDirectory
    ordering = ('-updated',)
    create_view_class = EventDirectoryCreateView
    edit_view_class = EventDirectoryEditView
    menu_label = _('Event Directory')
    menu_icon = 'folder'
    menu_order = 100
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('event', 'link', 'description', 'creator',
                    'updated', 'created')
    search_fields = ('event', 'description')
    list_export = ('event', 'link', 'description')
    export_filename = 'Event_directory'


class EventDirectoryFileAdmin(ModelAdmin):
    model = EventDirectoryFile
    ordering = ('-updated',)
    create_view_class=EventDirectoryFileCreateView
    button_helper_class = EventDirectoryHelper
    menu_label = _('Event Directory Upload')
    menu_icon = 'folder'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('attachment', 'line_count', 'is_valid', 'creator',
                    'updated', 'created', )
    list_filter = ('is_valid', )
    search_fields = ('attachment', )


class EventDirectoryAdminGroup(ModelAdminGroup):
    menu_label = _('Event Directory')
    menu_icon = 'folder-open-inverse'
    menu_order = 200
    items = (EventDirectoryAdmin, EventDirectoryFileAdmin,)


modeladmin_register(EventDirectoryAdminGroup)


@hooks.register('register_admin_urls')
def register_Event_url():
    return [
        path('event_directory/eventDirectoryfile/',
        include('event_directory.urls', namespace='event_directory')),
    ]
