from django.db import models

# Create your models here.


class Category(models.Model):
    """
    Lớp Category dùng để lưu trữ thông tin về danh mục.
    
    Thuộc tính:
        name (CharField): Tên danh mục.
        description (CharField): Mô tả danh mục.
        createAt (DateTimeField): Ngày tạo danh mục.
        updateAt (DateTimeField): Ngày cập nhật danh mục.
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
