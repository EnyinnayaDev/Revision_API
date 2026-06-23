from django.contrib import admin
from .models import Document, Revision
# Register your models here.

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)  
    
@admin.register(Revision)
class RevisionAdmin(admin.ModelAdmin):
    list_display = ("document", "created_at")
    search_fields = ("document__title",)