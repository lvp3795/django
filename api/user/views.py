from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model, logout, login
from django.views.decorators.csrf import csrf_exempt
import re
import random
# Create your views here.


def generate_session_token(lenght=10):
    """
    Chức năng: Hàm này sẽ tạo ra một session token ngẫu nhiên có độ dài mặc định là 10 ký tự.

    Input:
        length: int(Độ dài của session token, mặc định là 10)

    Output:
        str: Session token ngẫu nhiên
    """
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)]+[str(i) for i in range(10)]) for _ in range(lenght))


@csrf_exempt
def signin(request):
    """
    Hàm này được sử dụng để xác thực người dùng khi đăng nhập. Nếu người dùng hợp lệ và mật khẩu đúng, hàm sẽ trả về một token để xác thực người dùng trong các request sau.

    Input:
        request: HttpRequest object
            Yêu cầu POST gồm các tham số 'email' và 'password' để đăng nhập

    Output:
        JsonResponse: Trả về kết quả xác thực người dùng dưới dạng một Json object với các trường sau:
            - Nếu đăng nhập thành công: 
                {'token': 'Session token', 'user': 'Thông tin người dùng'}
            - Nếu có lỗi: 
                {'error': 'Thông báo lỗi'}
    """
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a post request with valid parameter only'})
    username = request.POST['email']
    password = request.POST['password']

    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", username):
        return JsonResponse({'error': 'Enter a valid email'})

    if len(password) < 3:
        return JsonResponse({'error': 'Password needs to be at least of 3 char'})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)
        if user.check_password(password):
            user_dict = UserModel.objects.filter(
                email=username).values().first()
            user_dict.pop('password')
            if user.session_token != "0":
                user.session_token = "0"
                user.save()
                return JsonResponse({'error': 'Previous session exists!'})
            token = generate_session_token()
            user.session_token = token
            user.save()
            login(request, user)
            return JsonResponse({'token': token, 'user': user_dict})
        else:
            return JsonResponse({'error': 'Invalid password'})

    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid Email'})


def signout(request, id):
    """
    Hàm này được sử dụng để đăng xuất người dùng và hủy bỏ token hiện tại của người dùng.

    Input:
        request: HttpRequest object
            Yêu cầu đăng xuất
        id: int
            ID của người dùng cần đăng xuất

    Output:
        JsonResponse: Trả về kết quả đăng xuất dưới dạng một Json object với các trường sau:
            - Nếu đăng xuất thành công: 
                {'success': 'Logout success'}
            - Nếu có lỗi: 
                {'error': 'Thông báo lỗi'}
    """
    logout(request)

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = "0"
        user.save()

    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid user ID'})

    return JsonResponse({'success': 'Logout success'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    # def create(self, request, *args, **kwargs):
    #     user = CustomUser.objects.create(**request.data)
    #     if user.is_superuser:
    #         user.is_superuser = False
    #         user.save()
    #     if user.is_staff:
    #         user.is_staff = False
    #         user.save()
    #     serializer = self.get_serializer(user)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
