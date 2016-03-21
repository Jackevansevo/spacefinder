from django.contrib import admin

from .models import Department, StudySpace, Rating, Student


class StudySpaceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('space_name',)}
    readonly_fields = ("avg_rating",)


class StudentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('user',)}


class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ("timestamp",)

admin.site.register(Department)
admin.site.register(StudySpace, StudySpaceAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Student, StudentAdmin)
