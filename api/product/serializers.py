from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """
    Lớp ProductSerializer dùng để chuyển đổi thông tin sản phẩm từ model sang dạng JSON và ngược lại.

    Thuộc tính:
        image (ImageField): Hình ảnh sản phẩm.
    """
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=True, required=False)

    class Meta:
        """
        Thuộc tính:
            model (Model): Lớp model sử dụng để tạo serializer.
            fields (tuple): Danh sách các trường của model sẽ được sử dụng trong serializer.
        """
        model = Product
        fields = ('id', 'name', 'description', 'price', 'image', 'category')
