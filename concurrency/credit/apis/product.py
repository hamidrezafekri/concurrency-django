from rest_framework import serializers, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from concurrency.api.mixins import ApiAuthMixin
from concurrency.credit.models import Product
from concurrency.credit.permissions import SellerPermission
from concurrency.credit.selectors.product import product_detail, avalible_product_list
from concurrency.credit.services.product import create_product, update_product


class ProductInputSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        decimal_places=2,
        max_digits=15,
        required=True,
    )
    is_active = serializers.BooleanField(default=True)


class ProductOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "seller", "amount", "is_active", "created_at", "updated_at")


class ProductApi(ApiAuthMixin, APIView):
    permission_classes = (SellerPermission,)

    @extend_schema(request=ProductInputSerializer, responses=ProductOutSerializer)
    def post(self, request):
        serializer = ProductInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            print(request.user)
            product = create_product(
                seller=request.user,
                amount=serializer.validated_data.get("amount"),
                is_active=serializer.validated_data.get("is_active")
            )
            response_data = ProductOutSerializer(product).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"error": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailApi(ApiAuthMixin, APIView):
    permission_classes = (SellerPermission,)

    @extend_schema(responses=ProductOutSerializer)
    def get(self, request, id):
        try:
            product = product_detail(seller=request.user, id=id)
        except Exception as ex:
            return Response({"error": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProductOutSerializer(product).data, status=status.HTTP_200_OK)

    @extend_schema(request=ProductInputSerializer, responses=ProductOutSerializer)
    def put(self, request, id):
        serializer = ProductInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product = update_product(id=id,
                                     amount=serializer.validated_data.get("amount"),
                                     is_active=serializer.validated_data.get("is_active"))
            return Response(ProductInputSerializer(product).data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)


class ProductListApi(APIView):

    @extend_schema(responses=ProductOutSerializer)
    def get(self, request):
        try:
            products = avalible_product_list()
        except Exception as ex:
            return Response({"error": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProductOutSerializer(products).data, status=status.HTTP_200_OK)
