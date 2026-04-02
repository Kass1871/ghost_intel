from django.test import TestCase
from apps.core.models import Weapon


class WeaponModelTest(TestCase):

    #PreCondition
    #Sets up an environment for testing
    def setUp(self):
        # Testing data
        self.weapon_data = {
            "name": "Aisha's Care",
            "weapon_type": "Primary"
        }
        # Creating a model test object, saving it to the database, appending the object to the attribute of parent class
        self.weapon = Weapon.objects.create(**self.weapon_data)

    def test_create_weapon(self):
        """Testing if the data created successfully"""
        saved_weapon = Weapon.objects.get(id=self.weapon.id)
        #assert methods - waiting for a condition
        self.assertIsNotNone(saved_weapon)
        self.assertEqual(saved_weapon.name, self.weapon_data["name"])
        self.assertEqual(saved_weapon.weapon_type, self.weapon_data["weapon_type"])
        #Possible to do via __eq__ if such method is made in the model

    def test_update_weapon(self):
        """Testing that the client is being updated successfully"""
        self.weapon.name = "Zaouli’s Bane"
        self.weapon.save()
        updated_weapon = Weapon.objects.get(id=self.weapon.id)
        self.assertIsNotNone(updated_weapon)
        self.assertEqual(updated_weapon.name, "Zaouli’s Bane")

    def test_delete_client(self):
        """Testing that the client is being deleted successfully"""
        client_id = self.weapon.id
        self.weapon.delete()
        with self.assertRaises(Weapon.DoesNotExist):
            Weapon.objects.get(id=client_id)

    #PostCondition
    #Brings the environment back to its original state
    def tearDown(self):
        pass