from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from django.urls import reverse

from products.models import Product, Brand, Producer, Flavor, Nicotine
from products.serializers import ProductSerializer


class ProductsApiTestCase(APITestCase):
    def setUp(self):
        self.nic_content_1 = Nicotine.objects.create(amount='0')
        self.nic_content_2 = Nicotine.objects.create(amount='3')
        self.nic_content_3 = Nicotine.objects.create(amount='20 HARD')

        self.flavor_1 = Flavor.objects.create(name='Flavor 1')
        self.flavor_2 = Flavor.objects.create(name='Flavor 2')
        self.flavor_3 = Flavor.objects.create(name='Flavor 3')

        self.producer_1 = Producer.objects.create(
            name='Test producer 1',
            country='Country 1',
            description='Test producer 1 description',
            slug='producer_1'
        )
        self.producer_2 = Producer.objects.create(
            name='Test producer 2',
            country='Country 2',
            description='Test producer 2 description',
            slug='producer_2'
        )
        self.brand_1 = Brand.objects.create(
            name='Test brand 1',
            description='Test brand 1 description',
            producer=self.producer_1,
            slug='brand_1'
        )
        self.brand_2 = Brand.objects.create(
            name='Test brand 2',
            description='Test brand 2 description',
            producer=self.producer_2,
            slug='brand_2'
        )

        self.product_1 = Product.objects.create(
            name='Test product 1',
            brand=self.brand_1,
            description='Test product 1 description',
            is_salt=True,
            slug='product_1',
            is_published=True
        )
        self.product_1.nic_content.add(self.nic_content_1, self.nic_content_3)
        self.product_1.flavors.add(self.flavor_1, self.flavor_3)

        self.product_2 = Product.objects.create(
            name='Test product 2',
            brand=self.brand_2,
            description='Test product 2 description',
            is_salt=False,
            slug='product_2',
            is_published=True
        )
        self.product_2.nic_content.add(self.nic_content_1, self.nic_content_2)
        self.product_2.flavors.add(self.flavor_1, self.flavor_2)

        self.product_3 = Product.objects.create(
            name='Test product 3',
            brand=self.brand_2,
            description='Test product 3 description',
            is_salt=False,
        )
        self.product_3.nic_content.add(self.nic_content_3)
        self.product_3.flavors.add(self.flavor_2, self.flavor_3)

    def test_list(self):
        url = reverse('products')
        response = self.client.get(url)
        serializer_data = ProductSerializer([self.product_2, self.product_1], many=True).data
        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        url = reverse('products')
        data = {
            'name': 'Test product 3',
            'brand_id': self.brand_2.id,
            'description': 'Test product 3 description',
            'is_salt': 'false',
            'nic_content_id': [self.nic_content_2.id,  self.nic_content_3.id],
            'flavor_id': [self.flavor_1.id, self.flavor_2.id],
        }
        response = self.client.post(url, data=data)
        self.assertEqual(HTTP_201_CREATED, response.status_code)
        self.assertTrue(Product.objects.get(id=response.data['id']))
        self.assertFalse(Product.objects.get(id=response.data['id']).is_published)
    
    def test_filter_by_brand(self):
        url = reverse('products')
        response = self.client.get(url, {'brand__slug': self.brand_2.slug})
        self.assertEqual(HTTP_200_OK, response.status_code)
        qs = Product.objects.filter(brand__slug=self.brand_2.slug).filter(is_published=True)
        serializer_data = ProductSerializer(qs, many=True).data
        self.assertEqual(serializer_data, response.data)

