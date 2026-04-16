from django.test import TestCase
from apps.core.models import Exotic


class ExoticModelTest(TestCase):

    #PreCondition
    #Sets up an environment for testing
    def setUp(self):
        # Testing data
        self.exotic_data = {
            "name": "Monte Carlo",
            "type": "weapon"
        }
        # Creating a model test object, saving it to the database, appending the object to the attribute of parent class
        self.exotic = Exotic.objects.create(**self.exotic_data)

    def test_create_exotic(self):
        """Testing if the data created successfully"""
        saved_exotic = Exotic.objects.get(id=self.exotic.id)
        #assert methods - waiting for a condition
        self.assertIsNotNone(saved_exotic)
        self.assertEqual(saved_exotic.name, self.exotic_data["name"])
        self.assertEqual(saved_exotic.type, self.exotic_data["type"])
        #Possible to do via __eq__ if such method is made in the model

    def test_update_exotic(self):
        """Testing that the client is being updated successfully"""
        self.exotic.name = "Aeon Safe"
        self.exotic.type = "armor"
        self.exotic.save()
        updated_exotic = Exotic.objects.get(id=self.exotic.id)
        self.assertIsNotNone(updated_exotic)
        self.assertEqual(updated_exotic.name, "Aeon Safe")
        self.assertEqual(updated_exotic.type, "armor")

    def test_delete_exotic(self):
        """Testing that the client is being deleted successfully"""
        exotic_id = self.exotic.id
        self.exotic.delete()
        with self.assertRaises(Exotic.DoesNotExist):
            Exotic.objects.get(id=exotic_id)

    #PostCondition
    #Brings the environment back to its original state
    def tearDown(self):
        pass