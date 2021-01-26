import json

from django.db.models import Count
from django.http import JsonResponse

from rest_framework import permissions, status, viewsets
from rest_framework_jwt.settings import api_settings

from bakery.authenticate import AuthBackend
import bakery.serializers as serializers
import bakery.models as models


class LoginUser(viewsets.ViewSet):
    """
    View to register user.

    * Requires email and password.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Return user if login with token else error.
        """

        received_data = json.loads(request.body)

        email = received_data.get('email', None)
        password = received_data.get('password', None)

        if email is None or password is None:
            message = 'Please provide both email address and password'

            return JsonResponse(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call authbackend class from backends.py file for custom authentication
        Auth = AuthBackend()
        user = Auth.authenticate(email=email, password=password)

        if not user:
            message = 'Invalid credentials'

            return JsonResponse(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user = serializers.UserSerializer(user)

        return JsonResponse(
            {'token': token, 'user': user.data},
            status=status.HTTP_200_OK
        )


class RegisterUser(viewsets.ViewSet):
    """
    View to register user.

    * Requires email and password.
    * Name(optional)
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Return user if registered with token else error.
        """

        received_data = json.loads(request.body)

        email = received_data.get('email', None)
        password = received_data.get('password', None)
        name = received_data.get('name', None)

        if email is None or password is None:
            message = 'Please provide both email address and password'

            return JsonResponse(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call authbackend class from backends.py file for custom authentication
        Auth = AuthBackend()
        user = Auth.get_user_by_email(email=email)

        if user:
            message = 'Email already used'

            return JsonResponse(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = models.User()
        user.email = email
        user.set_password(password)
        user.name = name
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user = serializers.UserSerializer(user)

        return JsonResponse(
            {'token': token, 'user': user.data},
            status=status.HTTP_200_OK
        )


class BakeryIngredientViewSet(viewsets.ViewSet):
    """
    View to add and get list of ingredients.

    * Requires name, is_available, available_quantity for adding a ingredient.
    """
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        queryset = models.BakeryIngredient.objects\
            .filter(is_available=True)\
            .filter(available_quantity__gt=0.0)

        serializer = serializers.BakeryIngredientSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        received_data = json.loads(request.body)

        serializer = serializers.BakeryIngredientSerializer(data=received_data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(
                serializer.data,
                safe=False,
                status=status.HTTP_201_CREATED
            )

        return JsonResponse(
            serializer.errors,
            safe=False,
            status=status.HTTP_400_BAD_REQUEST
        )


class BakeryItemViewSet(viewsets.ViewSet):
    """
    View to get all and single bakery item
    """

    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = models.BakeryItem.objects\
            .filter(available_quantity__gt=0.0)

        serializer = serializers.BakeryItemSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)

    def retrieve(self, request, pk=None):
        queryset = models.BakeryItem.objects\
            .get(id=pk)

        serializer = serializers.BakeryItemSerializer(queryset, many=False)

        return JsonResponse(serializer.data, safe=False)


class AddBakeryItemViewSet(viewsets.ViewSet):
    """
    View to add bakery item.

    * Requires name, available_quantity, cost_price, selling_price.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        received_data = json.loads(request.body)

        serializer = serializers.BakeryItemSerializer(data=received_data)

        if serializer.is_valid():
            serializer.save()

            bakery_item_data = serializer.data

            ingredients = received_data.get('ingredients', [])

            total_percent = 0

            for ingredient in ingredients:
                i = models.BakeryItemIngredient()

                i.bakery_item = models.BakeryItem.objects.get(id=bakery_item_data['id'])
                i.bakery_ingredient = models.BakeryIngredient.objects \
                    .get(id=ingredient.get('bakery_ingredient', None))

                quantity_percent = ingredient.get('quantity_percent', None)

                i.quantity_percent = quantity_percent

                total_percent += quantity_percent

                if total_percent > 100:
                    break

                i.save()

            bakery_item = models.BakeryItem.objects.get(id=bakery_item_data['id'])
            bakery_item = serializers.BakeryItemSerializer(bakery_item)

            return JsonResponse(
                bakery_item.data,
                safe=False,
                status=status.HTTP_201_CREATED
            )

        return JsonResponse(
            serializer.errors,
            safe=False,
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderItemViewSet(viewsets.ViewSet):
    """
    View to add and get list of ingredients.

    * Requires name, is_available, available_quantity for adding a ingredient.
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        orders = models.Order.objects.filter(user=request.user)

        serializer = serializers.OrderSerializer(orders, many=True)

        return JsonResponse(
            serializer.data,
            safe=False,
            status=status.HTTP_201_CREATED
        )


    def post(self, request):
        received_data = json.loads(request.body)

        bakery_item = received_data.get('bakery_item', None)
        quantity = received_data.get('quantity', None)

        if not (bakery_item or quantity):
            return JsonResponse(
                {'message': 'No bakery item in cart'},
                safe=False,
                status=status.HTTP_400_BAD_REQUEST
            )

        bakery_item = models.BakeryItem.objects.get(id=bakery_item)

        received_data['user'] = request.user.id
        received_data['bakery_item'] = bakery_item.id
        received_data['price'] = bakery_item.selling_price

        serializer = serializers.OrderSerializer(data=received_data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(
                serializer.data,
                safe=False,
                status=status.HTTP_201_CREATED
            )

        return JsonResponse(
            serializer.errors,
            safe=False,
            status=status.HTTP_400_BAD_REQUEST
        )


class TrendingItemViewSet(viewsets.ViewSet):
    """
    View to add and get list of ingredients.

    * Requires name, is_available, available_quantity for adding a ingredient.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = models.Order.objects.values('bakery_item').order_by().annotate(item_count=Count('bakery_item'))
        trending_item = max(orders, key=lambda x: x['item_count'])

        item = models.BakeryItem.objects.get(id=trending_item['bakery_item'])

        serializer = serializers.BakeryItemSerializer(item, many=False)

        return JsonResponse(
            serializer.data,
            safe=False,
            status=status.HTTP_201_CREATED
        )


