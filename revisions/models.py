from django.db import models

# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Revision(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="revisions")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Revision for {self.document.title} at {self.created_at}"