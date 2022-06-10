from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK
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

        # self.product_1 = Product.objects.create(
        #     name='Test product 1',
        #     brand=self.brand_1,
        #     description='Test product 1 description',
        #     is_salt=True,
        #     slug='product_1',
        #     is_published=True
        # )
        # self.product_1.nic_content.add(self.nic_content_1, self.nic_content_3)
        # self.product_1.flavors.add(self.flavor_1, self.flavor_3)

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
        print(response.data)
        serializer_data = ProductSerializer([self.product_2], many=True).data
        print(serializer_data)
        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(serializer_data, response.data)