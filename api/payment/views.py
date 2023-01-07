from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import braintree
# Create your views here.

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="fy9wx3swcr756b5c",
        public_key="mwh3477xtpxs68d3",
        private_key="b974927f7d8243a08f9cd3c3e1f0bcc8"
    )
)


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
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False


@csrf_exempt
def generate_token(request, id, token):
    """
    Chức năng: Tạo mã phiên làm việc cho người dùng dựa trên yêu cầu POST.

    Input:
        request (Request): Đối tượng yêu cầu.
        id (int): Khóa chính của người dùng.
        token (str): Mã phiên làm việc cần được xác minh.

    Output:
        JsonResponse: Chứa mã phiên làm việc mới được tạo và thông báo về kết quả.
    """
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Invalid session token, Please login again'})

    return JsonResponse({'clientToken': gateway.client_token.generate(), 'success': True})


@csrf_exempt
def process_payment(request, id, token):
    """
    Chức năng: Xử lý thanh toán cho người dùng dựa trên yêu cầu POST.

    Tham số:
        request (Request): Đối tượng yêu cầu.
        id (int): Khóa chính của người dùng.
        token (str): Mã phiên làm việc cần được xác minh.

    Trả về:
        JsonResponse: Chứa thông tin về kết quả thanh toán và mã giao dịch.
    """
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Invalid session token, Please login again'})

    nonce_from_the_client = request.POST['paymentMethodNonce']
    amount_from_the_client = request.POST['amount']

    result = gateway.transaction.sale({
        "amount": amount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        return JsonResponse({'success': result.is_success, 'transaction': {'id': result.transaction.id, 'amount': result.transaction.amount}})
    else:
        return JsonResponse({'error': True, 'success': False})
