"""
Custom Permissions
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to interact with it.
    """

    message = {"You are not the owner of this wallet."}

    def has_object_permission(self, request, view, obj):
        """check that wallet owner is current user"""
        return obj.user == request.user


class IsSenderOwner(permissions.BasePermission):
    """
    Check that the user is the owner of the sender wallet
    """

    message = "You are not the owner of this sender wallet."

    def has_object_permission(self, request, view, obj):
        """check that transaction's sender is current user"""
        return obj.sender.user == request.user


class IsSenderOrReceiverOwner(permissions.BasePermission):
    """
    Permission that check that either sender wallet or receiver wallet
    belongs to the current user
    """

    message = "You are not the owner of the wallet."

    def has_object_permission(self, request, view, obj):
        """check that transaction's sender or receiver is current user"""
        return obj.sender.user == request.user or obj.receiver.user == request.user
