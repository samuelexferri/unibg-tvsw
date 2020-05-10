from unittest import TestCase

from mock import MagicMock

from pharmacies.permission import *

"""
Permission tests (Mock)
"""


class TestPermissions(TestCase):
    def test_permissions_IsAdmin_true(self):
        self.request = MagicMock(user=MagicMock())
        self.request.user.is_superuser = True
        self.view = MagicMock()
        self.assertTrue(IsAdmin.has_permission(self, self.request, self.view))

    def test_permissions_IsAdmin_false(self):
        self.request = MagicMock(user=MagicMock())
        self.request.user.is_superuser = False
        self.view = MagicMock()
        self.assertFalse(IsAdmin.has_permission(self, self.request, self.view))

    def test_permissions_IsStaff_true(self):
        self.request = MagicMock(user=MagicMock())
        self.request.user.is_staff = True
        self.view = MagicMock()
        self.assertTrue(IsStaff.has_permission(self, self.request, self.view))

    def test_permissions_IsStaff_false(self):
        self.request = MagicMock(user=MagicMock())
        self.request.user.is_staff = False
        self.view = MagicMock()
        self.assertFalse(IsStaff.has_permission(self, self.request, self.view))

    def test_permissions_IsAdminOrReadOnly_true(self):
        self.request = MagicMock(user=MagicMock())
        self.request.user.is_superuser = True
        self.view = MagicMock()
        self.assertTrue(
            IsAdminOrReadOnly.has_permission(self, self.request, self.view)
        )

    def test_permissions_IsAdminOrReadOnly_false(self):
        self.request = MagicMock(user=MagicMock())
        self.request.user.is_superuser = False
        self.view = MagicMock()
        self.assertFalse(
            IsAdminOrReadOnly.has_permission(self, self.request, self.view)
        )

    def test_permissions_IsStaffOrReadOnly_true(self):
        self.request = MagicMock(user=MagicMock())
        self.request.user.is_staff = True
        self.view = MagicMock()
        self.assertTrue(
            IsStaffOrReadOnly.has_permission(self, self.request, self.view)
        )

    def test_permissions_IsStaffOrReadOnly_false(self):
        self.request = MagicMock(user=MagicMock())
        self.request.user.is_staff = False
        self.view = MagicMock()
        self.assertFalse(
            IsStaffOrReadOnly.has_permission(self, self.request, self.view)
        )

    def test_permissions_IsAuthenticatedOrReadOnly_true(self):
        self.request = MagicMock(user=MagicMock())
        self.request.user.is_authenticated = True
        self.view = MagicMock()
        self.assertTrue(
            IsAuthenticatedOrReadOnly.has_permission(
                self, self.request, self.view
            )
        )

    def test_permissions_IsAuthenticatedOrReadOnly_false(self):
        self.request = MagicMock(user=MagicMock())
        self.request.user.is_authenticated = False
        self.view = MagicMock()
        self.assertFalse(
            IsAuthenticatedOrReadOnly.has_permission(
                self, self.request, self.view
            )
        )
