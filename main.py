import requests
import os
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('site', nargs='?')
    return parser


def count_clicks(headers, url_for_clicks_count):
    clicks_count = requests.get(url_for_clicks_count, headers=headers)
    clicks_count.raise_for_status()
    clicks_count = clicks_count.json()
    return clicks_count


def shorten_link(headers, url_for_short_links, payload):
    response = requests.post(url_for_short_links, headers=headers, json=payload)
    response.raise_for_status()
    response = response.json()
    return response['link']


def check_the_link_for_short(headers, url_for_bitlink_info):
    bitlink_info = requests.get(url_for_bitlink_info, headers=headers)
    bitlink_info = bitlink_info.ok
    return bitlink_info


def main():
    parser = createParser()
    namespace = parser.parse_args()
    link = namespace.site
    url_for_short_links = 'https://api-ssl.bitly.com/v4/shorten'
    parsed_link_from_user = urlparse(link)
    link_to_check_for_short = '{}{}'.format(parsed_link_from_user.netloc, parsed_link_from_user.path)
    url_for_bitlink_info = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(link_to_check_for_short)

    headers = {
        'Authorization': os.getenv('BITLY_TOKEN')
    }
    payload = {
        'long_url': link
    }

    short_link_check = check_the_link_for_short(headers, url_for_bitlink_info)

    if short_link_check:
        url_for_clicks_count = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(link_to_check_for_short)

        try:
            clicks_count = count_clicks(headers, url_for_clicks_count)
            print('По вашей ссылке прошли ', clicks_count['total_clicks'], 'раз(а)')
        except requests.exceptions.HTTPError:
            print('Ошибка!!!!!')
        
    else:
        try:
            bitlink = shorten_link(headers, url_for_short_links, payload=payload)
            print('Короткая ссылка:', bitlink)
        except requests.exceptions.HTTPError:
            print('Ошибка!!!!!!')
        
       
if __name__ == "__main__":
    load_dotenv()
    main()