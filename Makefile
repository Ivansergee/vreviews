run_django:
	cd reviews_django; python manage.py runserver

run_vue:
	cd reviews_vue; npm run serve

scp_django:
	scp -r /home/ivan/reviews/reviews_django/products ivan@188.68.223.142:/var/www/vaperate/reviews_django/

scp_vue:
	scp -r /home/ivan/reviews/reviews_vue/dist ivan@188.68.223.142:/var/www/vaperate/reviews_vue/