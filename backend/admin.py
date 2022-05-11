from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Project, Document, Annotation

# Register your models here.
@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    pass
