from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    """
    Lớp CustomUser kế thừa từ AbstractUser và dùng để lưu trữ thông tin về người dùng.

    Thuộc tính:
        name (CharField): Tên người dùng.
        email (EmailField): Email người dùng.
        username (None): Không sử dụng username như lớp AbstractUser.
        USERNAME_FIELD (str): Sử dụng email làm tên đăng nhập.
        REQUIRED_FIELDS (list): Danh sách các trường bắt buộc phải có.
        phone (CharField): Số điện thoại người dùng.
        gender (CharField): Giới tính người dùng.
        session_token (CharField): Mã phiên làm việc của người dùng.
        createAt (DateTimeField): Thời gian khởi tạo.
        updateAt (DateTimeField): Thời gian cập nhật.
    """
    name = models.CharField(max_length=50, default='User')
    email = models.EmailField(max_length=100, unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [name, email]
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    session_token = models.CharField(max_length=10, default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
