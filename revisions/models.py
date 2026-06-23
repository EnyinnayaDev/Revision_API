from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Revision(models.Model):
    document = models.ForeignKey(
        Document, related_name="revisions", on_delete=models.CASCADE
    )
    revision_number = models.PositiveIntegerField()
    content = models.TextField()
    created_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["revision_number"]
        unique_together = ("document", "revision_number")

    def save(self, *args, **kwargs):
        if self.revision_number is None:
            last = (
                Revision.objects
                .filter(document=self.document)
                .order_by("-revision_number")
                .first()
            )
            self.revision_number = (last.revision_number + 1) if last else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.document.title} - rev {self.revision_number}"