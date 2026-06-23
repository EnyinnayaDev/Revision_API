from rest_framework import serializers
from .models import Document, Revision


class RevisionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = ["id", "revision_number", "created_by", "created_at"]