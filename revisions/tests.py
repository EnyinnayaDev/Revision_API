from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Document, Revision

# Create your tests here.
class CompareRevisionsTests(APITestCase):
    def setUp(self):
        self.doc1 = Document.objects.create(title="Doc One")
        self.doc2 = Document.objects.create(title="Doc Two")

        self.rev1 = Revision.objects.create(
            document=self.doc1, content="line one\nline two\nline three"
        )
        self.rev2 = Revision.objects.create(
            document=self.doc1, content="line one\nline two edited\nline three"
        )
        self.other_doc_rev = Revision.objects.create(
            document=self.doc2, content="unrelated content"
        )

    def test_valid_compare_returns_diff(self):
        url = f"/compare?from={self.rev1.id}&to={self.rev2.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("diff", response.data)
        self.assertEqual(response.data["document_id"], self.doc1.id)

    def test_missing_from_param_returns_400(self):
        response = self.client.get(f"/compare?to={self.rev2.id}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_to_param_returns_400(self):
        response = self.client.get(f"/compare?from={self.rev1.id}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonexistent_revision_returns_404(self):
        response = self.client.get(f"/compare?from=9999&to={self.rev2.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cross_document_compare_rejected(self):
        url = f"/compare?from={self.rev1.id}&to={self.other_doc_rev.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_self_compare_has_no_changes(self):
        url = f"/compare?from={self.rev1.id}&to={self.rev1.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # No '+' or '-' prefixed lines should exist when comparing a revision to itself
        changed_lines = [
            line for line in response.data["diff"]
            if line.startswith("+ ") or line.startswith("- ")
        ]
        self.assertEqual(changed_lines, [])

    def test_diff_direction_is_symmetric(self):
        forward = self.client.get(
            f"/compare?from={self.rev1.id}&to={self.rev2.id}"
        ).data["diff"]
        backward = self.client.get(
            f"/compare?from={self.rev2.id}&to={self.rev1.id}"
        ).data["diff"]

        forward_added = [l[2:] for l in forward if l.startswith("+ ")]
        forward_removed = [l[2:] for l in forward if l.startswith("- ")]
        backward_added = [l[2:] for l in backward if l.startswith("+ ")]
        backward_removed = [l[2:] for l in backward if l.startswith("- ")]

        # What was "added" going forward should be "removed" going backward, and vice versa
        self.assertEqual(forward_added, backward_removed)
        self.assertEqual(forward_removed, backward_added)