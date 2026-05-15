"""
Test cases for smart_lock_management_plugin models.
"""

from django.core.exceptions import ValidationError

from ..models import Smart_Lock_Management_Plugin
from ..testing import PluginModelTestCase
from ..testing.utils import create_tags, get_random_string


class Smart_Lock_Management_PluginTestCase(PluginModelTestCase):
    """Test Smart_Lock_Management_Plugin model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        # Create test instances
        Smart_Lock_Management_Plugin.objects.create(name='Test 1')
        Smart_Lock_Management_Plugin.objects.create(name='Test 2')
        Smart_Lock_Management_Plugin.objects.create(name='Test 3')

    def test_create_smartlockmanagementplugin(self):
        """Test creating a Smart_Lock_Management_Plugin instance."""
        name = f'Test {get_random_string(10)}'
        instance = Smart_Lock_Management_Plugin.objects.create(name=name)

        self.assertEqual(instance.name, name)
        self.assertIsNotNone(instance.pk)

    def test_smartlockmanagementplugin_str(self):
        """Test Smart_Lock_Management_Plugin string representation."""
        instance = Smart_Lock_Management_Plugin.objects.first()
        self.assertEqual(str(instance), instance.name)

    def test_smartlockmanagementplugin_absolute_url(self):
        """Test Smart_Lock_Management_Plugin get_absolute_url method."""
        instance = Smart_Lock_Management_Plugin.objects.first()
        url = instance.get_absolute_url()

        self.assertIsNotNone(url)
        self.assertIn(str(instance.pk), url)

    def test_smartlockmanagementplugin_unique_name(self):
        """Test that Smart_Lock_Management_Plugin names must be unique."""
        name = 'Duplicate Name'
        Smart_Lock_Management_Plugin.objects.create(name=name)

        with self.assertRaises(ValidationError):
            instance = Smart_Lock_Management_Plugin(name=name)
            instance.full_clean()

    def test_model_to_dict(self):
        """Test model_to_dict helper method."""
        instance = Smart_Lock_Management_Plugin.objects.first()
        data = self.model_to_dict(instance)

        self.assertIn('name', data)
        self.assertEqual(data['name'], instance.name)
        self.assertIn('id', data)

    def test_instance_equal(self):
        """Test assertInstanceEqual helper method."""
        instance = Smart_Lock_Management_Plugin.objects.first()

        # Should pass with matching data
        self.assertInstanceEqual(
            instance,
            {'name': instance.name, 'id': instance.pk}
        )

    def test_smartlockmanagementplugin_with_tags(self):
        """Test Smart_Lock_Management_Plugin with tags."""
        tags = create_tags(['important', 'test'])
        instance = Smart_Lock_Management_Plugin.objects.first()

        instance.tags.add(*tags)
        instance.save()

        self.assertEqual(instance.tags.count(), 2)
        self.assertIn(tags[0], instance.tags.all())

    def test_bulk_create(self):
        """Test bulk creation of Smart_Lock_Management_Plugin instances."""
        initial_count = Smart_Lock_Management_Plugin.objects.count()

        instances = [
            Smart_Lock_Management_Plugin(name=f'Bulk {i}')
            for i in range(5)
        ]
        Smart_Lock_Management_Plugin.objects.bulk_create(instances)

        self.assertEqual(
            Smart_Lock_Management_Plugin.objects.count(),
            initial_count + 5
        )

    def test_query_filter(self):
        """Test filtering Smart_Lock_Management_Plugin instances."""
        # Create a specific instance for filtering
        test_name = f'FilterTest {get_random_string(10)}'
        Smart_Lock_Management_Plugin.objects.create(name=test_name)

        # Test filter
        results = Smart_Lock_Management_Plugin.objects.filter(name=test_name)
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().name, test_name)

    def test_ordering(self):
        """Test Smart_Lock_Management_Plugin default ordering."""
        instances = list(Smart_Lock_Management_Plugin.objects.all())

        # Check that instances are ordered by name
        names = [instance.name for instance in instances]
        self.assertEqual(names, sorted(names))


class Smart_Lock_Management_PluginValidationTestCase(PluginModelTestCase):
    """Test Smart_Lock_Management_Plugin validation."""

    def test_empty_name(self):
        """Test that empty name is not allowed."""
        with self.assertRaises(ValidationError):
            instance = Smart_Lock_Management_Plugin(name='')
            instance.full_clean()

    def test_name_max_length(self):
        """Test name field max length."""
        long_name = 'x' * 101  # Exceeds max_length of 100

        with self.assertRaises(ValidationError):
            instance = Smart_Lock_Management_Plugin(name=long_name)
            instance.full_clean()
