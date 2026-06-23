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


@api_view(["GET"])
def compare_revisions(request):
    from_id = request.query_params.get("from")
    to_id = request.query_params.get("to")

    # 1. Both params must be present
    if not from_id or not to_id:
        return Response(
            {"error": "Both 'from' and 'to' query parameters are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 2. Both revisions must exist
    try:
        from_rev = Revision.objects.get(id=from_id)
    except Revision.DoesNotExist:
        return Response(
            {"error": f"Revision {from_id} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        to_rev = Revision.objects.get(id=to_id)
    except Revision.DoesNotExist:
        return Response(
            {"error": f"Revision {to_id} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # 3. Must belong to the same document
    if from_rev.document_id != to_rev.document_id:
        return Response(
            {"error": "Cannot compare revisions from different documents"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 4. Diff the content
    diff = list(difflib.ndiff(
        from_rev.content.splitlines(),
        to_rev.content.splitlines(),
    ))

    return Response({
        "document_id": from_rev.document_id,
        "from": {"id": from_rev.id, "revision_number": from_rev.revision_number},
        "to": {"id": to_rev.id, "revision_number": to_rev.revision_number},
        "diff": diff,
    })