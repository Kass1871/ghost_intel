from uuid import uuid4
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.text import slugify
from apps.core.models import Build, Tag, Weapon, Exotic
class BuildModelTest(TestCase):

    #PreCondition
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='fridge', password='testPass')
        cls.tag1 = Tag.objects.create(name="PvE")
        cls.tag2 = Tag.objects.create(name="Hunter")
        cls.weapon1 = Weapon.objects.create(name="Aisha's Care", weapon_type="primary")
        cls.weapon2 = Weapon.objects.create(name="Forbearance", weapon_type="special")
        cls.exotic = Exotic.objects.create(name="Celestial Nighthawk", type="armor")

    #Sets up an environment for testing
    def setUp(self):
        # Testing data
        title = "Stasis Hunter Build"
        self.build_data = {
            "title": title,
            "slug": f"{slugify(title)}-{uuid4().hex[:8]}",
            "description": "Some stuff we made up",
            "content": "Random build",
            "author": self.user,
            "status": "archived",
            "build_class": "hunter",
            "subclass": "stasis",
            "build_type": "pve",
            "difficulty": "beginner",
            "expansion": "Renegades",
            "views": 0
        }
        # Creating a model test object, saving it to the database, appending the object to the attribute of parent class
        self.build = Build.objects.create(**self.build_data)

    def test_create_build(self):
        """Testing if the data created successfully"""
        saved_build = Build.objects.get(id=self.build.id)
        #assert methods - waiting for a condition
        self.assertIsNotNone(saved_build)
        self.assertEqual(saved_build.title, self.build_data["title"])
        self.assertEqual(saved_build.slug, self.build_data["slug"])
        self.assertEqual(saved_build.description, self.build_data["description"])
        self.assertEqual(saved_build.content, self.build_data["content"])
        self.assertEqual(saved_build.author, self.build_data["author"])
        self.assertEqual(saved_build.status, self.build_data["status"])
        self.assertEqual(saved_build.build_class, self.build_data["build_class"])
        self.assertEqual(saved_build.subclass, self.build_data["subclass"])
        self.assertEqual(saved_build.build_type, self.build_data["build_type"])
        self.assertEqual(saved_build.difficulty, self.build_data["difficulty"])
        self.assertEqual(saved_build.expansion, self.build_data["expansion"])
        self.assertEqual(saved_build.views, self.build_data["views"])
        #Possible to do via __eq__ if such method is made in the model

    def test_add_m2m(self):
        build = self.build
        build.weapons.add(self.weapon1, self.weapon2)
        build.exotics.add(self.exotic)
        build.tags.add(self.tag1, self.tag2)
        build.likes.add(self.user)

        self.assertEqual(build.weapons.count(), 2)
        self.assertTrue(build.weapons.filter(pk=self.weapon1.pk).exists())
        self.assertEqual(build.exotics.count(), 1)
        self.assertEqual(build.tags.count(), 2)
        self.assertEqual(build.likes.count(), 1)

    def test_update_build(self):
        """Testing that the client is being updated successfully"""
        self.build.build_class = "Titan"
        self.build.build_type = "pvp"
        self.build.views = 200
        self.build.save()
        updated_build = Build.objects.get(id=self.build.id)
        self.assertIsNotNone(updated_build)
        self.assertEqual(updated_build.build_class, "Titan")
        self.assertEqual(updated_build.build_type, "pvp")
        self.assertEqual(updated_build.views, 200)

    def test_set_remove_clear_m2m(self):
        build = self.build
        build.weapons.set([self.weapon1, self.weapon2])
        build.weapons.remove(self.weapon2)
        self.assertQuerySetEqual(build.weapons.order_by("id"), [self.weapon1])
        build.weapons.clear()
        self.assertEqual(build.weapons.count(), 0)

    def test_delete_build(self):
        """Testing that the client is being deleted successfully"""
        build_id = self.build.id
        self.build.delete()
        with self.assertRaises(Build.DoesNotExist):
            Build.objects.get(id=build_id)

    #PostCondition
    #Brings the environment back to its original state
    def tearDown(self):
        pass