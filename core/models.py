from django.db import models
import os
import pdfplumber
from django.core.files.uploadedfile import UploadedFile

def document_upload_path(instance, filename):
    # Flat folder for development/MVP
    # Later: can use uuid or date after first save
    return f'documents/{filename}'

class Document(models.Model):
    title       = models.CharField(max_length=255, blank=True)
    file        = models.FileField(upload_to=document_upload_path, null=True, blank=True)
    content     = models.TextField(blank=True)
    file_name   = models.CharField(max_length=255, blank=True)
    mime_type   = models.CharField(max_length=100, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    # ... rest of the model unchanged ...

    def __str__(self):
        return self.title or self.file_name or f"Doc {self.id}"

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Step 1: Capture MIME type BEFORE saving (while it's still UploadedFile)
        if self.file and isinstance(self.file, UploadedFile):
            self.mime_type = self.file.content_type or self.guess_mime_type()
            self.file_name = self.file.name

        # Step 2: Save the model (this writes file to disk)
        super().save(*args, **kwargs)

        # Step 3: Extract text AFTER file is on disk (path exists)
        if self.file and self.file.path:
            # Only re-extract if content is empty or file changed
            if not self.content or (self.pk and Document.objects.get(pk=self.pk).file != self.file):
                self.extract_text()
                # Save again to store extracted content (only once)
                super().save(update_fields=['content', 'title'])

    def guess_mime_type(self):
        """Fallback if content_type not available"""
        ext = os.path.splitext(self.file.name)[1].lower()
        if ext == '.pdf':
            return 'application/pdf'
        # Add more extensions if you support other formats later
        return 'application/octet-stream'

    def extract_text(self):
        if not self.file or not self.file.path:
            self.content = "[No file path available]"
            return

        try:
            with pdfplumber.open(self.file.path) as pdf:
                pages_text = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pages_text.append(text.strip())
                
                full_text = "\n\n".join(pages_text)
                self.content = full_text[:500000]  # hard limit to avoid huge docs

                # Auto-set title if empty
                if not self.title:
                    self.title = os.path.splitext(self.file_name)[0].replace('_', ' ').title()

        except Exception as e:
            self.content = f"[Extraction failed: {str(e)}]"