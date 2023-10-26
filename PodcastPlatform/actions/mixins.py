from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.authentications import JWTAuthentication


class InteractionMixin:
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    action_model = None
    model = None


    def post(self, request, **kwargs):
        pk = request.data.get('pk')

        item = self.model.objects.get(pk=pk)
        content_type = ContentType.objects.get_for_model(item)

        _, created = self.action_model.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=item.pk,
            **kwargs
        )

        if not created:
            return Response({'message': f"You've already interacted with this item."},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': f"Your object has been created successfully ."}, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        pk = request.data.get('pk')

        item = self.model.objects.get(id=pk)

        try:
            content_type = ContentType.objects.get_for_model(item)

            interaction = self.action_model.objects.get(user=request.user,
                                            content_type=content_type,
                                            object_id=item.pk, )
            interaction.delete()

            return Response({'message': f"Your object has been deleted ."}, status=status.HTTP_200_OK)
        except self.action_model.DoesNotExist:
            return Response({'message': "You haven't interacted with this item."}, status=status.HTTP_400_BAD_REQUEST)

