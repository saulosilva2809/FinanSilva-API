from rest_framework import permissions


class IsTransactionOnwer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.account.user == request.user


class IsTransferOnwer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.original_account.user == request.user
