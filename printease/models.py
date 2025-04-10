from django.db import models



class UserModel(models.Model):
    email = models.EmailField(max_length=278)
    password = models.CharField(max_length=80)

    def __str__(self):
        return f"user model {self.email}"

class FilesUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserModel, related_name="files_upload", on_delete=models.CASCADE)

    def __str__(self):
        return f"File uploaded by {self.user.email if self.user else 'Unknown'} on {self.uploaded_at}"


class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(default='default@example.com')
    phone = models.CharField(max_length=15)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    notes = models.TextField(blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserModel, related_name="order", on_delete=models.CASCADE)

    def __str__(self):
        return f"Order by {self.name} ({self.product_name or 'No Product Specified'})"
