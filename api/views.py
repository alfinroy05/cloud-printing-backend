from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.


# ✅ User Registration API
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)




# ✅ User Login API
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        user = authenticate(username=user.username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
    except User.DoesNotExist:
        pass

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Welcome to Web2Print API!"})


from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import PrintOrder
from .serializers import PrintOrderSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # ✅ Require authentication
@parser_classes([MultiPartParser, FormParser])
def upload_file(request):
    print("✅ Received Upload Request")

    if 'file' not in request.FILES:
        print("❌ No file found in request")
        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']
    page_size = request.data.get('page_size', 'A4')
    num_copies = request.data.get('num_copies', '1')
    print_type = request.data.get('print_type', 'black_white')

    user = request.user  # ✅ Get authenticated user
    print(f"👤 User: {user}")

    try:
        print_order = PrintOrder.objects.create(
            user=user,
            file=file,
            file_name=file.name,
            file_path=f"uploads/{file.name}",
            page_size=page_size,
            num_copies=num_copies,
            print_type=print_type
        )
        print("✅ Print Order Created:", print_order)

    except Exception as e:
        print("❌ Error saving order:", str(e))
        return Response({'error': 'Could not save order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'message': 'File uploaded successfully',
        'order_id': print_order.id,
        'file_name': print_order.file_name,
        'page_size': print_order.page_size,
        'num_copies': print_order.num_copies,
        'print_type': print_order.print_type,
    }, status=status.HTTP_201_CREATED)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PrintOrder
from .serializers import PrintOrderSerializer

@api_view(['GET'])
def get_orders(request):
    orders = PrintOrder.objects.all().order_by('-id')  # ✅ Fetch all print orders (latest first)
    serializer = PrintOrderSerializer(orders, many=True)  # ✅ Convert to JSON
    return Response(serializer.data)
