from django.db import models
from django.contrib.auth.models import User


# class UserModel(models.Model):
#     email = models.EmailField(max_length=278,unique=True)
#     password = models.CharField(max_length=80)
#     date_joined= models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"user model {self.email}"

class FilesUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="files_upload", on_delete=models.CASCADE)

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
    product_type = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="order", on_delete=models.CASCADE)

    def __str__(self):
        return f"Order by {self.name} ({self.product_name or 'No Product Specified'})"


class OrderBillModel(models.Model):

    order_type=models.CharField(max_length=600)
    company_name=models.CharField(max_length=100)
    address=models.CharField(max_length=1000)
    paper_type=models.CharField(max_length=100)
    paper_size=models.CharField(max_length=50)
    quantity=models.PositiveIntegerField(default=1, null=True)
    number_of_book = models.IntegerField(default=1, null=True)
    page_per_book = models.IntegerField(default=1, null=True)
    user=models.ForeignKey(User, related_name="order_bill_model", on_delete=models.CASCADE)

    logo = models.ImageField(
        upload_to='billbook_logos/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"File uploaded by {self.order_type} on {self.company_name}"


class OrderLetterModel(models.Model):
    PAPER_TYPE_CHOICES = [
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
    ]

    PAPER_SIZE_CHOICES = [
        ('A4', 'A4 (210 × 297 mm)'),
        ('Letter', 'Letter (8.5 × 11 inches)'),
    ]

    order_type = models.CharField(max_length=600, default='Letterhead')
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    paper_type = models.CharField(max_length=100, choices=PAPER_TYPE_CHOICES)
    paper_size = models.CharField(max_length=50, choices=PAPER_SIZE_CHOICES)
    quantity = models.PositiveIntegerField(default=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='letterhead_logos/', blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.paper_type} Letterhead"