from celery import shared_task
from django.core.mail import send_mail

import requests
from bs4 import BeautifulSoup

from task.models import Quote, Author


@shared_task
def get_quotes():
    main_url = 'https://quotes.toscrape.com'
    counter = 0

    url = main_url
    while True:
        r = requests.get(url)
        bs_content = BeautifulSoup(r.content, 'parser.html')
        quotes = bs_content.find_all('div')
        for quote in quotes:
            q_text = quote.get('text')
            if Quote.objects.filter(text=q_text).exists():
                continue

            author_url = main_url + quote.get('author url')
            r_author = requests.get(author_url)
            bs_author = BeautifulSoup(r_author.content, 'parser.html')

            author, created = Author.objects.get_or_create(
                name=bs_author.get('author_name'),
                defaults={
                    'bio': bs_author.get('author_bio')
                }
            )

            Quote.objects.create(text=q_text, author=author)
            counter += 1
            if counter == 5:
                break

        p_number_element = BeautifulSoup.content.get('p_number_element')
        if p_number_element:
            p_number = p_number_element.get('p_number')
            url = main_url + p_number
        else:
            send_mail('Task is done', 'There is no quotes left', 'admin@gmail.com', 'admin@gmail.com',
                      fail_silently=False)
            break

