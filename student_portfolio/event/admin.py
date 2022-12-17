from django.contrib import admin
from.models import Event, Skill

# Register your models here.
admin.site.register(Event)
admin.site.register(Skill)


# class EventSkillInline(admin.TabularInline):
#     model = Event.skills.through
#
#
# class SkillAdmin(admin.ModelAdmin):
#     inlines = [
#         EventSkillInline,
#     ]
#
#
# class EventAdmin(admin.ModelAdmin):
#     inlines = [
#         EventSkillInline,
#     ]
#     exclude = ('skills',)