"""
Test cases for smart_lock_management_plugin views.
"""

from django.urls import reverse

from ..models import Smart_Lock_Management_Plugin
from ..testing import PluginViewTestCase
from ..testing.utils import disable_warnings, get_random_string


class Smart_Lock_Management_PluginViewTestCase(PluginViewTestCase):
    """Test Smart_Lock_Management_Plugin views."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        Smart_Lock_Management_Plugin.objects.create(name='View Test 1')
        Smart_Lock_Management_Plugin.objects.create(name='View Test 2')
        Smart_Lock_Management_Plugin.objects.create(name='View Test 3')

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.base_url = 'plugins:smart_lock_management_plugin:smartlockmanagementplugin'

    def test_list_smartlockmanagementplugins(self):
        """Test Smart_Lock_Management_Plugin list view."""
        self.add_permissions('smart_lock_management_plugin.view_smartlockmanagementplugin')

        url = reverse('plugins:smart_lock_management_plugin:smartlockmanagementplugin_list')
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)

    def test_list_smartlockmanagementplugins_without_permission(self):
        """Test Smart_Lock_Management_Plugin list view without permission."""
        url = reverse('plugins:smart_lock_management_plugin:smartlockmanagementplugin_list')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_view_smartlockmanagementplugin(self):
        """Test Smart_Lock_Management_Plugin detail view."""
        self.add_permissions('smart_lock_management_plugin.view_smartlockmanagementplugin')

        instance = Smart_Lock_Management_Plugin.objects.first()
        url = reverse('plugins:smart_lock_management_plugin:smartlockmanagementplugin', kwargs={'pk': instance.pk})
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.context['object'], instance)

    def test_create_smartlockmanagementplugin(self):
        """Test creating a Smart_Lock_Management_Plugin via form."""
        self.add_permissions(
            'smart_lock_management_plugin.add_smartlockmanagementplugin',
            'smart_lock_management_plugin.view_smartlockmanagementplugin'
        )

        url = reverse('plugins:smart_lock_management_plugin:smartlockmanagementplugin_add')
        name = f'Created {get_random_string(10)}'

        form_data = self.post_data({
            'name': name,
        })

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        # Verify object was created
        instance = Smart_Lock_Management_Plugin.objects.get(name=name)
        self.assertEqual(instance.name, name)

    def test_create_smartlockmanagementplugin_without_permission(self):
        """Test creating a Smart_Lock_Management_Plugin without permission."""
        url = reverse('plugins:smart_lock_management_plugin:smartlockmanagementplugin_add')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_edit_smartlockmanagementplugin(self):
        """Test editing a Smart_Lock_Management_Plugin via form."""
        self.add_permissions(
            'smart_lock_management_plugin.change_smartlockmanagementplugin',
            'smart_lock_management_plugin.view_smartlockmanagementplugin'
        )

        instance = Smart_Lock_Management_Plugin.objects.first()
        url = reverse('plugins:smart_lock_management_plugin:smartlockmanagementplugin_edit', kwargs={'pk': instance.pk})

        new_name = f'Edited {get_random_string(10)}'
        form_data = self.post_data({
            'name': new_name,
        })

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        # Verify object was updated
        instance.refresh_from_db()
        self.assertEqual(instance.name, new_name)

    def test_delete_smartlockmanagementplugin(self):
        """Test deleting a Smart_Lock_Management_Plugin."""
        self.add_permissions(
            'smart_lock_management_plugin.delete_smartlockmanagementplugin',
            'smart_lock_management_plugin.view_smartlockmanagementplugin'
        )

        instance = Smart_Lock_Management_Plugin.objects.first()
        url = reverse('plugins:smart_lock_management_plugin:smartlockmanagementplugin_delete', kwargs={'pk': instance.pk})

        # Confirm deletion
        response = self.client.post(url, {'confirm': True}, follow=True)
        self.assertHttpStatus(response, 200)

        # Verify object was deleted
        self.assertFalse(
            Smart_Lock_Management_Plugin.objects.filter(pk=instance.pk).exists()
        )

    def test_delete_smartlockmanagementplugin_without_permission(self):
        """Test deleting a Smart_Lock_Management_Plugin without permission."""
        instance = Smart_Lock_Management_Plugin.objects.first()
        url = reverse('plugins:smart_lock_management_plugin:smartlockmanagementplugin_delete', kwargs={'pk': instance.pk})

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)


class Smart_Lock_Management_PluginFormTestCase(PluginViewTestCase):
    """Test Smart_Lock_Management_Plugin form validation."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.add_permissions(
            'smart_lock_management_plugin.add_smartlockmanagementplugin',
            'smart_lock_management_plugin.view_smartlockmanagementplugin'
        )

    def test_form_validation_empty_name(self):
        """Test form validation with empty name."""
        url = reverse('plugins:smart_lock_management_plugin:smartlockmanagementplugin_add')
        form_data = self.post_data({'name': ''})

        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 200)  # Form redisplay

        # Should not create object
        self.assertEqual(Smart_Lock_Management_Plugin.objects.filter(name='').count(), 0)

    def test_form_validation_duplicate_name(self):
        """Test form validation with duplicate name."""
        Smart_Lock_Management_Plugin.objects.create(name='Duplicate')

        url = reverse('plugins:smart_lock_management_plugin:smartlockmanagementplugin_add')
        form_data = self.post_data({'name': 'Duplicate'})

        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 200)  # Form redisplay

        # Should only have one instance with this name
        self.assertEqual(Smart_Lock_Management_Plugin.objects.filter(name='Duplicate').count(), 1)
