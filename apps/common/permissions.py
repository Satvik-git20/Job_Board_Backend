from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCandidate(BasePermission):
    """
    Allows access only to authenticated users with the 'candidate' role.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'candidate'
        )

class IsEmployer(BasePermission):
    """
    Allows access only to authenticated users with the 'employer' role.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'employer'
        )

class IsAdminUserRole(BasePermission):
    """
    Allows access only to authenticated users with the 'admin' role or staff privileges.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role == 'admin' or request.user.is_staff or request.user.is_superuser)
        )

class IsEmployerOwner(BasePermission):
    """
    Object-level permission to only allow employer owner of a job to view/edit it.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'employer')

    def has_object_permission(self, request, view, obj):
        # obj.employer is an EmployerProfile which has a user field
        if hasattr(obj, 'employer'):
            return obj.employer.user == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        return False

class IsCandidateOwner(BasePermission):
    """
    Object-level permission for candidates managing their own items (resumes, applications, saved jobs).
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'candidate')

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'candidate'):
            return obj.candidate.user == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        return False
