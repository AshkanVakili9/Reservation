from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view
from drf_spectacular.utils import extend_schema


@extend_schema(responses=UserSerializer)
@api_view(["GET"])
@permission_classes([AllowAny])
def create(request):
    queryset = get_user_model().objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)
