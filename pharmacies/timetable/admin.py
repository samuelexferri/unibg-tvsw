from django.contrib import admin

from timetable.models import Timetable


class TimetableAdmin(admin.ModelAdmin):
    readonly_fields = ['day', 'slot4h']

    def has_add_permission(self, request):
        return False


admin.site.register(Timetable, TimetableAdmin)
