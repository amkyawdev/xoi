"""Permission management"""

from enum import Enum
from typing import Any


class Permission(Enum):
    """Permission types"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"


class Role:
    """Role with permissions"""
    
    def __init__(self, name: str, permissions: list[Permission]):
        self.name = name
        self.permissions = permissions
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if role has permission"""
        return permission in self.permissions


class PermissionManager:
    """Manage roles and permissions"""
    
    def __init__(self):
        self.roles: dict[str, Role] = {
            "user": Role("user", [Permission.READ]),
            "editor": Role("editor", [Permission.READ, Permission.WRITE]),
            "admin": Role("admin", [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN])
        }
        self.user_roles: dict[str, str] = {}
    
    def assign_role(self, user_id: str, role_name: str) -> None:
        """Assign role to user"""
        if role_name in self.roles:
            self.user_roles[user_id] = role_name
    
    def get_role(self, user_id: str) -> Role | None:
        """Get user role"""
        role_name = self.user_roles.get(user_id)
        return self.roles.get(role_name)
    
    def has_permission(self, user_id: str, permission: Permission) -> bool:
        """Check if user has permission"""
        role = self.get_role(user_id)
        return role.has_permission(permission) if role else False


# Global permission manager
permissions = PermissionManager()
