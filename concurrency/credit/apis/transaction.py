from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from concurrency.api.mixins import ApiAuthMixin
from concurrency.credit.models import CreditRequest
from concurrency.credit.permissions import AdminPermission
from concurrency.credit.services.transaction import approve_request, reject_request


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
                credit_request = approve_request(id=id)
                return Response({"message": "request updated successfully"}, status=status.HTTP_200_OK)
            else:
                credit_request = reject_request(id=id)
                return Response({"message": "request updated successfully"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)
