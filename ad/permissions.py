from rest_framework.permissions import BasePermission

from ad.models import Ad
from users.models import User, UserRoles


# class SelectionActionsPermission(BasePermission):
# 	message = 'You do not have permission to do this'
#
# 	def has_permission(self, request, view):
# 		try:
# 			selection = Selection.objects.get(id=view.kwargs['pk'])
# 		except Selection.DoesNotExist:
# 			return False
#
# 		return request.user.id == selection.owner.id


class IsOwnerOrAdmin(BasePermission):
	message = 'You do not have permission to do this'

	def has_permission(self, request, view):
		try:
			ad = Ad.objects.get(id=view.kwargs['pk'])
		except Ad.DoesNotExist:
			return False

		if request.user.id == ad.author.id:
			return True
		elif request.user.role == UserRoles.ADMIN.value:
			return True
		return False
