from rest_framework import generics
from users.models import Member
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated

class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
