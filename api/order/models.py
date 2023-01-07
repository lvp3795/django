from django.db import models
from api.user.models import CustomUser
from api.product.models import Product
# Create your models here.


class Order(models.Model):
    """
    Lớp Order dùng để lưu trữ thông tin về đơn hàng.
    
    Thuộc tính:
        user (ForeignKey): Liên kết tới người dùng tạo đơn hàng.
        product_names (CharField): Tên các sản phẩm trong đơn hàng.
        total_product (CharField): Tổng số lượng sản phẩm trong đơn hàng.
        transaction_id (CharField): Mã giao dịch của đơn hàng.
        total_amount (CharField): Tổng tiền của đơn hàng.
        createAt (DateTimeField): Ngày tạo đơn hàng.
        updateAt (DateTimeField): Ngày cập nhật đơn hàng.
    """
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    product_names = models.CharField(max_length=500)
    total_product = models.CharField(max_length=500, default=0)
    transaction_id = models.CharField(max_length=150, default=0)
    total_amount = models.CharField(max_length=50, default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_id
