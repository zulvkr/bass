

from rest_framework.response import Response
from common.serializers import UserSerializer
from core.models import User
from rest_framework.views import APIView


class AmbassadorAPIView(APIView):

  def get(self, _):
    ambassadors = User.objects.filter(is_ambassador=True)
    serializer = UserSerializer(ambassadors, many=True)
    return Response(serializer.data)