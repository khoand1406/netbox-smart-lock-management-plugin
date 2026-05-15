"""
Test cases for smart_lock_management_plugin GraphQL API.
"""
from ..models import Smart_Lock_Management_Plugin
from ..testing import PluginGraphQLTestCase


class Smart_Lock_Management_PluginGraphQLTestCase(PluginGraphQLTestCase):
    """Test Smart_Lock_Management_Plugin GraphQL queries."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        Smart_Lock_Management_Plugin.objects.create(name='GraphQL Test 1')
        Smart_Lock_Management_Plugin.objects.create(name='GraphQL Test 2')
        Smart_Lock_Management_Plugin.objects.create(name='GraphQL Test 3')

    def test_query_smartlockmanagementplugin(self):
        """Test GraphQL query for a single Smart_Lock_Management_Plugin."""
        self.add_permissions('smart_lock_management_plugin.view_smartlockmanagementplugin')

        instance = Smart_Lock_Management_Plugin.objects.first()

        query = (
            "query { "
            "smartlockmanagementplugin(id: " + str(instance.pk) + ") { "
            "id name "
            "} "
            "}"
        )

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['smartlockmanagementplugin']
        self.assertEqual(data['id'], str(instance.pk))
        self.assertEqual(data['name'], instance.name)

    def test_query_smartlockmanagementplugin_list(self):
        """Test GraphQL query for list of Smart_Lock_Management_Plugins."""
        self.add_permissions('smart_lock_management_plugin.view_smartlockmanagementplugin')

        query = """
        query {
            smartlockmanagementplugin_list {
                id
                name
            }
        }
        """

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['smartlockmanagementplugin_list']
        self.assertEqual(len(data), 3)
        self.assertIn('id', data[0])
        self.assertIn('name', data[0])

    def test_query_smartlockmanagementplugin_with_all_fields(self):
        """Test GraphQL query with all available fields."""
        self.add_permissions('smart_lock_management_plugin.view_smartlockmanagementplugin')

        instance = Smart_Lock_Management_Plugin.objects.first()

        query = (
            "query { "
            "smartlockmanagementplugin(id: " + str(instance.pk) + ") { "
            "id name created last_updated "
            "} "
            "}"
        )

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['smartlockmanagementplugin']
        self.assertEqual(data['id'], str(instance.pk))
        self.assertEqual(data['name'], instance.name)
        self.assertIsNotNone(data['created'])
        self.assertIsNotNone(data['last_updated'])

