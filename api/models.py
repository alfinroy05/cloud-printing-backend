from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PrintOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ✅ Link order to user
    file = models.FileField(upload_to='uploads/')  # ✅ File upload field
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    page_size = models.CharField(max_length=10, choices=[('A4', 'A4'), ('A3', 'A3')])
    num_copies = models.IntegerField(default=1)
    print_type = models.CharField(max_length=20, choices=[('black_white', 'Black & White'), ('color', 'Color')])
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('printing', 'Printing'), ('completed', 'Completed')],
        default='pending'
    )  # ✅ Track order status
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} - {self.page_size} - {self.num_copies} copies - {self.status}"
