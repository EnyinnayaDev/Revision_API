from django.shortcuts import render
import difflib

from .models import Revision

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Document
from .serializers import RevisionListSerializer


@api_view(["GET"])
def revision_list(request, doc_id):
    try:
        document = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        return Response(
            {"error": f"Document {doc_id} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    revisions = document.revisions.all()
    serializer = RevisionListSerializer(revisions, many=True)
    return Response(serializer.data)