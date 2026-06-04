# todolist/api/tasks/task_logo.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser


class TaskLogo(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes  = [ JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        if 'avatar' not in request.FILES:
            return Response({'error': 'No image provided'}, status=400)

        user        = request.user
        user.avatar = request.FILES['avatar']
        user.save()

        return Response({
            'message': 'Avatar uploaded successfully',
            'avatar':  request.build_absolute_uri(user.avatar.url)
        }, status=200)