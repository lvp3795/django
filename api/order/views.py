from rest_framework import viewsets
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .serializers import OrderSerializer
from .models import Order
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def validate_user_session(id, token):
    """
    Chức năng: Xác minh phiên làm việc của người dùng bằng cách kiểm tra token.

    Input:
        id (int): Khóa chính của người dùng.
        token (str): Mã phiên làm việc cần được xác minh.

    Output:
        bool: True nếu mã phiên làm việc là hợp lệ, ngược lại là False.
    """
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        if (user.session_token == token):
            return True
        return False
    except UserModel.DoesNotExist:
        return False


@csrf_exempt
def add(request, id, token):
    """
    Chức năng: Thêm đơn hàng cho người dùng dựa trên yêu cầu POST.

    Tham số:
        request (Request): Đối tượng yêu cầu.
        id (int): Khóa chính của người dùng.
        token (str): Mã phiên làm việc.

    Trả về:
        JsonResponse: Chứa thông báo về kết quả thêm đơn hàng.
    """
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Please re-login'})
    if request.method == "POST":
        user_id = id
        transaction_id = request.POST['transaction_id']
        amount = request.POST['amount']
        products = request.POST['products']
        total_product = len(products.split(',')[:-1])

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'})

        order = Order(user=user, product_names=products, total_product=total_product,
                      transaction_id=transaction_id, total_amount=amount)
        order.save()
        return JsonResponse({'success': True, 'error': False, 'msg': 'Order placed successfully'})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer
