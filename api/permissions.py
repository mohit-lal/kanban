from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Column
from django.shortcuts import get_object_or_404

class IsAuthenticatedAndHasAccessColumn(IsAuthenticated):
    def has_permission(self, request, view):
        """
            checks if the user if authenticated.
            If the user is authenticated then check if the user
            has access to column.
        """
        
        has_permission = super().has_permission(request, view)

        meta = vars(request)

        if has_permission:
            pk = meta.get('parser_context').get('kwargs')['pk']
            user = meta.get('_user')
            if not hasattr(self, 'column'):
                self.column = get_object_or_404(Column, pk=pk)

            if self.column.created_by == user:
                return True

            members = self.column.board.members.all()

            if user in members:
                return True

        return False


        