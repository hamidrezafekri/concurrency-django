from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from concurrency.api.mixins import ApiAuthMixin
from concurrency.credit.models import CreditRequest
from concurrency.credit.permissions import AdminPermission, CustomerPermission
from concurrency.credit.selectors.product import check_product_avaliblity
from concurrency.credit.services.transaction import approve_request, reject_request, sell_product


class ChangeRequestStatusApi(ApiAuthMixin, APIView):
    permission_classes = (AdminPermission,)

    class ChangeRequestInPutSerializer(serializers.Serializer):
        status = serializers.BooleanField(required=True)

    class ChangeRequestOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = CreditRequest
            fields = ('id', "amount", "seller", "created_at", "updated_at")

    @extend_schema(request=ChangeRequestInPutSerializer)
    def put(self, request, id):
        serializer = self.ChangeRequestInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            if serializer.validated_data.get("status"):
                approve_request(id=id)
                return Response({"message": "request updated successfully"}, status=status.HTTP_200_OK)
            else:
                reject_request(id=id)
                return Response({"message": "request updated successfully"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)


class BuyCreditApi(ApiAuthMixin, APIView):
    permission_classes = (CustomerPermission,)

    class BuyInPutSerializer(serializers.Serializer):
        product = serializers.IntegerField(required=True)

    @extend_schema(request=BuyInPutSerializer)
    def post(self, request):
        serializer = self.BuyInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            if not check_product_avaliblity(id=serializer.validated_data.get("product")):
                return Response({"message": "product is not avalible"}, status=status.HTTP_400_BAD_REQUEST)
            sell_product(customer=request.user,
                         product_id=serializer.validated_data.get("product"))
            return Response({"message": "your phone charge increased"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)
