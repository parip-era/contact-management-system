import tempfile
import unittest
from pathlib import Path

from contact_manager import ContactManager


class ContactManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database_path = Path(self.temp_dir.name) / "test_contacts.db"
        self.manager = ContactManager(database_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_get_contact(self):
        contact_id = self.manager.add_contact(
            "Alex Smith",
            "555-0100",
            "alex@example.com",
            "Main Street",
        )

        contacts = self.manager.get_all_contacts()

        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0][0], contact_id)
        self.assertEqual(contacts[0][1], "Alex Smith")

    def test_search_contact(self):
        self.manager.add_contact("Alex Smith", "555-0100")
        results = self.manager.search_contacts("Alex")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Alex Smith")

    def test_update_and_delete_contact(self):
        contact_id = self.manager.add_contact("Alex Smith", "555-0100")

        updated = self.manager.update_contact(
            contact_id,
            "Alex Jones",
            "555-0199",
        )
        self.assertTrue(updated)
        self.assertEqual(self.manager.get_all_contacts()[0][1], "Alex Jones")

        deleted = self.manager.delete_contact(contact_id)
        self.assertTrue(deleted)
        self.assertEqual(self.manager.get_all_contacts(), [])

    def test_invalid_email_is_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.add_contact("Alex Smith", "555-0100", "not-an-email")


if __name__ == "__main__":
    unittest.main()
