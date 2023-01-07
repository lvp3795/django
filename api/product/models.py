from django.db import models
from api.category.models import Category

# Create your models here.


class Product(models.Model):
    """
    Lớp Product dùng để lưu trữ thông tin về sản phẩm.

    Thuộc tính:
        name (CharField): Tên sản phẩm.
        description (CharField): Mô tả sản phẩm.
        price (CharField): Giá sản phẩm.
        stock (CharField): Số lượng sản phẩm trong kho.
        isActive (BooleanField): Trạng thái của sản phẩm.
        image (ImageField): Hình ảnh sản phẩm.
        category (ForeignKey): Liên kết tới danh mục của sản phẩm.
        createAt (DateTimeField): Ngày tạo sản phẩm.
        updateAt (DateTimeField): Ngày cập nhật sản phẩm.
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.CharField(max_length=50)
    stock = models.CharField(max_length=50)
    isActive = models.BooleanField(default=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
