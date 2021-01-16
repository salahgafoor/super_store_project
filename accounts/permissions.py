from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """"Allow user to edit their own profile"""
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id    #if user id matches the profile id, then returns true

class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""
    def has_object_permission(self, request, view, obj):
        """Check user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile.id == request.user.id
        
        
class IsOwnerAndAuth(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            return obj.user.user == request.user
        except:
            return False

    def has_permission(self, request, view):
        print("Error heereee")
        print(request.user)
        if request.user and request.user.is_authenticated():
            return True
        return False        