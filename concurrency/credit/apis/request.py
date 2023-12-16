from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from concurrency.api.mixins import ApiAuthMixin
from concurrency.credit.permissions import SellerPermission
from concurrency.credit.models import CreditRequest
from concurrency.credit.selectors.request import seller_request_list
from concurrency.credit.services.request import request_increase_credit


class CreditRequestApi(ApiAuthMixin, APIView):
    permission_classes = (SellerPermission,)

    class RequestInPutSerializer(serializers.Serializer):
        amount = serializers.DecimalField(max_digits=15, decimal_places=2)

    class RequsetOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = CreditRequest
            fields = ("id", "amount", "status", "created_at", "updated_at")

    @extend_schema(request=RequestInPutSerializer, responses=RequsetOutPutSerializer)
    def post(self, request):
        serializer = self.RequestInPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            request_object = request_increase_credit(
                seller=request.user,
                amount=serializer.validated_data.get("amount")
            )
        except Exception as ex:
            return Response({"error": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.RequsetOutPutSerializer(request_object).data, status=status.HTTP_201_CREATED)

    @extend_schema(responses=RequsetOutPutSerializer)
    def get(self, request):
        try:
            requests = seller_request_list(seller=request.user)
        except Exception as ex:
            return Response({"error": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.RequsetOutPutSerializer(requests).data, status=status.HTTP_200_OK)
