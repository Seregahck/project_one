"""
Тесты для классов Product и Category
"""
import pytest
from main import Product, Category


@pytest.fixture
def sample_product():
    """Фикстура для создания тестового продукта"""
    return Product("Телефон", "Смартфон", 50000.0, 10)


@pytest.fixture
def sample_products():
    """Фикстура для создания списка тестовых продуктов"""
    return [
        Product("Телефон", "Смартфон", 50000.0, 10),
        Product("Ноутбук", "Мощный ноутбук", 80000.0, 5),
        Product("Планшет", "Компактный планшет", 30000.0, 7)
    ]


@pytest.fixture
def sample_category(sample_products):
    """Фикстура для создания тестовой категории с продуктами"""
    return Category("Электроника", "Электронные товары", sample_products)


@pytest.fixture
def empty_category():
    """Фикстура для создания пустой категории"""
    return Category("Пустая категория", "Категория без товаров")


def test_product_initialization(sample_product):
    """Тест проверки корректности инициализации объектов класса Product"""
    assert sample_product.name == "Телефон"
    assert sample_product.description == "Смартфон"
    assert sample_product.price == 50000.0
    assert sample_product.quantity == 10


def test_product_initialization_with_different_values():
    """Тест проверки инициализации продукта с другими значениями"""
    product = Product("Ноутбук", "Мощный ноутбук для игр", 80000.0, 5)
    assert product.name == "Ноутбук"
    assert product.description == "Мощный ноутбук для игр"
    assert product.price == 80000.0
    assert product.quantity == 5


def test_category_initialization(sample_category, sample_products):
    """Тест проверки корректности инициализации объектов класса Category"""
    assert sample_category.name == "Электроника"
    assert sample_category.description == "Электронные товары"
    assert len(sample_category.products) == 3
    assert sample_category.products == sample_products


def test_category_initialization_without_products(empty_category):
    """Тест проверки инициализации категории без товаров"""
    assert empty_category.name == "Пустая категория"
    assert empty_category.description == "Категория без товаров"
    assert len(empty_category.products) == 0
    assert isinstance(empty_category.products, list)


def test_category_initialization_with_none_products():
    """Тест проверки инициализации категории с None вместо списка"""
    category = Category("Тестовая категория", "Описание", None)
    assert len(category.products) == 0
    assert isinstance(category.products, list)


def test_product_count():
    """Тест проверки подсчета количества продуктов"""
    # Сброс счетчиков перед тестом
    Category.category_count = 0
    Category.product_count = 0

    # Создание продуктов
    product1 = Product("Товар 1", "Описание 1", 100.0, 1)
    product2 = Product("Товар 2", "Описание 2", 200.0, 2)
    product3 = Product("Товар 3", "Описание 3", 300.0, 3)

    # Создание первой категории с 2 продуктами
    category1 = Category("Категория 1", "Описание 1", [product1, product2])
    assert Category.product_count == 2

    # Создание второй категории с 1 продуктом
    category2 = Category("Категория 2", "Описание 2", [product3])
    assert Category.product_count == 3

    # Создание категории без продуктов
    category3 = Category("Категория 3", "Описание 3")
    assert Category.product_count == 3  # Количество не должно измениться


def test_category_count():
    """Тест проверки подсчета количества категорий"""
    # Сброс счетчиков перед тестом
    Category.category_count = 0
    Category.product_count = 0

    # Создание категорий
    category1 = Category("Категория 1", "Описание 1")
    assert Category.category_count == 1

    category2 = Category("Категория 2", "Описание 2")
    assert Category.category_count == 2

    category3 = Category("Категория 3", "Описание 3")
    assert Category.category_count == 3


def test_product_count_with_multiple_categories():
    """Тест проверки подсчета продуктов в нескольких категориях"""
    # Сброс счетчиков перед тестом
    Category.category_count = 0
    Category.product_count = 0

    # Создание продуктов
    products_category1 = [
        Product("Товар A1", "Описание", 100.0, 1),
        Product("Товар A2", "Описание", 200.0, 2)
    ]

    products_category2 = [
        Product("Товар B1", "Описание", 300.0, 3),
        Product("Товар B2", "Описание", 400.0, 4),
        Product("Товар B3", "Описание", 500.0, 5)
    ]

    # Создание категорий
    category1 = Category("Категория A", "Описание A", products_category1)
    category2 = Category("Категория B", "Описание B", products_category2)

    assert Category.product_count == 5  # 2 + 3 = 5
    assert Category.category_count == 2


def test_product_and_category_counts_integration():
    """Интеграционный тест подсчета продуктов и категорий"""
    # Сброс счетчиков перед тестом
    Category.category_count = 0
    Category.product_count = 0

    # Создание продуктов
    product1 = Product("Товар 1", "Описание 1", 100.0, 1)
    product2 = Product("Товар 2", "Описание 2", 200.0, 2)
    product3 = Product("Товар 3", "Описание 3", 300.0, 3)

    # Создание категорий
    category1 = Category("Категория 1", "Описание 1", [product1, product2])
    category2 = Category("Категория 2", "Описание 2", [product3])
    category3 = Category("Категория 3", "Описание 3")

    assert Category.category_count == 3
    assert Category.product_count == 3


def test_product_attributes_types(sample_product):
    """Тест проверки типов атрибутов продукта"""
    assert isinstance(sample_product.name, str)
    assert isinstance(sample_product.description, str)
    assert isinstance(sample_product.price, float)
    assert isinstance(sample_product.quantity, int)


def test_category_attributes_types(sample_category):
    """Тест проверки типов атрибутов категории"""
    assert isinstance(sample_category.name, str)
    assert isinstance(sample_category.description, str)
    assert isinstance(sample_category.products, list)
    assert isinstance(Category.category_count, int)
    assert isinstance(Category.product_count, int)


def test_class_attributes_are_class_level():
    """Тест проверки, что атрибуты класса действительно принадлежат классу"""
    # Проверка, что атрибуты доступны через класс
    assert hasattr(Category, 'category_count')
    assert hasattr(Category, 'product_count')

    # Проверка, что атрибуты доступны через экземпляр
    category = Category("Тест", "Описание")
    assert hasattr(category, 'category_count')
    assert hasattr(category, 'product_count')
