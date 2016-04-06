from django.contrib import admin

from .models import Department, StudySpace, Rating, Student


class StudySpaceAdmin(admin.ModelAdmin):
    list_display = ('space_name', 'department', 'avg_rating')
    prepopulated_fields = {'slug': ('space_name',)}
    readonly_fields = ("avg_rating",)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'karma')
    prepopulated_fields = {'slug': ('user',)}


class RatingAdmin(admin.ModelAdmin):
    list_display = ('rating', 'studyspace', 'student', 'timestamp')
    readonly_fields = ("timestamp",)

admin.site.register(Department)
admin.site.register(StudySpace, StudySpaceAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Student, StudentAdmin)
