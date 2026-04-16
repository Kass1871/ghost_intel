from django.contrib.auth.models import User
from django.test import TestCase
from apps.core.models import News
from uuid import uuid4
from django.utils.text import slugify

class NewsModelTest(TestCase):

    #PreCondition
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='fridge', password='testing')

        cls.news_a = News.objects.create(
            title="This week at Bungie",
            slug=f"{slugify('This week at Bungie')}-{uuid4().hex[:8]}",
            description="Event and stuff",
            content="A lot.",
            author=cls.user,
            status="published",
            category="weekly",
            source="Bungie",
            isGameBreaking=False,
        )

        cls.news_b = News.objects.create(
            title="Emergency Patch",
            slug=f"{slugify('Emergency Patch')}-{uuid4().hex[:8]}",
            description="Hotfix details",
            content="Fixed major issue.",
            author=cls.user,
            status="published",
            category="patch",
            source="Bungie",
            isGameBreaking=True,
        )

    #Sets up an environment for testing
    def setUp(self):
        # Testing data
        self.news_data = {
            "category": "event",
            "source": "Bungie",
            "isGameBreaking": False
        }
        # Creating a model test object, saving it to the database, appending the object to the attribute of parent class
        self.news = News.objects.create(**self.news_data)

    def test_create_news(self):
        """Testing if the data created successfully"""
        saved_news = News.objects.get(id=self.news.id)
        #assert methods - waiting for a condition
        self.assertIsNotNone(saved_news)
        self.assertEqual(saved_news.category, self.news_data["category"])
        self.assertEqual(saved_news.source, self.news_data["source"])
        self.assertEqual(saved_news.isGameBreaking, self.news_data["isGameBreaking"])
        #Possible to do via __eq__ if such method is made in the model

    def test_add_related_content(self):
        self.news_a.relatedContent.add(self.news_b)

        self.assertTrue(self.news_a.relatedContent.filter(pk=self.news_b.pk).exists())
        self.assertFalse(self.news_b.relatedContent.filter(pk=self.news_a.pk).exists())

    def test_remove_related_content(self):
        self.news_a.relatedContent.add(self.news_b)
        self.news_a.relatedContent.remove(self.news_b)

        self.assertFalse(self.news_a.relatedContent.filter(pk=self.news_b.pk).exists())

    def test_clear_related_content(self):
        self.news_a.relatedContent.add(self.news_b)
        self.news_a.relatedContent.clear()

        self.assertEqual(self.news_a.relatedContent.count(), 0)

    def test_update_news(self):
        """Testing that the client is being updated successfully"""
        self.news.category = "patch"
        self.news.save()
        updated_news = News.objects.get(id=self.news.id)
        self.assertIsNotNone(updated_news)
        self.assertEqual(updated_news.category, "patch")

    def test_delete_news(self):
        """Testing that the client is being deleted successfully"""
        news_id = self.news.id
        self.news.delete()
        with self.assertRaises(News.DoesNotExist):
            News.objects.get(id=news_id)

    #PostCondition
    #Brings the environment back to its original state
    def tearDown(self):
        pass