# installed
from django.test import TestCase
# local
from apps.orderserviceapi.models import Category


class CategoryModelTest(TestCase):
    def setUp(self):
        """
        Создание одной родительской и 2-х дочерних categories
        """
        self.parent_category = Category(
            name="parent_category"
        )
        self.child_category_1 = Category(
            name="child_category_1",
            parent=self.parent_category
        )
        self.child_category_2 = Category(
            name="child_category_2",
            parent=self.parent_category
        )

    def test_create_category(self):
        """
        Проверка создание categories и связей между ними
        """
        # сохраняем модели в БД
        self.parent_category.save()
        self.child_category_1.save()
        self.child_category_2.save()

        # получаем модели из БД
        parent_category = Category.objects.get(name=self.parent_category.name)
        child_category_1 = Category.objects.get(name=self.child_category_1.name)
        child_category_2 = Category.objects.get(name=self.child_category_2.name)

        # проверяем имена
        self.assertEqual(parent_category.name, "parent_category")
        self.assertEqual(child_category_1.name, "child_category_1")
        self.assertEqual(child_category_2.name, "child_category_2")

        # проверяем связи между categories
        self.assertEqual(parent_category.parent, None)
        self.assertEqual(child_category_1.parent, parent_category)
        self.assertEqual(child_category_2.parent, parent_category)