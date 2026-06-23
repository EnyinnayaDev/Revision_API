from django.urls import path
from . import views

urlpatterns = [
    path("docs/<int:doc_id>/revisions", views.revision_list, name="revision-list"),
]