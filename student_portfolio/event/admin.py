from django.contrib import admin
from.models import Event, Skill, EventAttendance, Curriculum, Skillgroup

# Register your models here.
admin.site.register(Event)
admin.site.register(Skill)
admin.site.register(EventAttendance)
admin.site.register(Curriculum)
admin.site.register(Skillgroup)
