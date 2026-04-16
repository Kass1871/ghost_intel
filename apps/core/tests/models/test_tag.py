from django.test import TestCase
from apps.core.models import Tag


class TagModelTest(TestCase):

    #PreCondition
    #Sets up an environment for testing
    def setUp(self):
        # Testing data
        self.tag_data = {
            "name": "Build"
        }
        # Creating a model test object, saving it to the database, appending the object to the attribute of parent class
        self.tag = Tag.objects.create(**self.tag_data)

    def test_create_tag(self):
        """Testing if the data created successfully"""
        saved_tag = Tag.objects.get(id=self.tag.id)
        #assert methods - waiting for a condition
        self.assertIsNotNone(saved_tag)
        self.assertEqual(saved_tag.name, self.tag_data["name"])
        #Possible to do via __eq__ if such method is made in the model

    def test_update_tag(self):
        """Testing that the client is being updated successfully"""
        self.tag.name = "News"
        self.tag.save()
        updated_tag = Tag.objects.get(id=self.tag.id)
        self.assertIsNotNone(updated_tag)
        self.assertEqual(updated_tag.name, "News")

    def test_delete_tag(self):
        """Testing that the client is being deleted successfully"""
        tag_id = self.tag.id
        self.tag.delete()
        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get(id=tag_id)

    #PostCondition
    #Brings the environment back to its original state
    def tearDown(self):
        pass