import argparse
import sys
import requests
import bs4


def is_comment(element):
    return isinstance(element, bs4.element.Comment)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="comment-reveal", add_help=True,
                                     description='Search for comments on given endpoints.')

    parser.add_argument('base_url', action='store', help='Url of website to crawl on')
    parser.add_argument('endpoint_file', action='store', help='File with website endpoints to search for comments on')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    options = parser.parse_args()
    base_url = options.base_url
    endpoint_file = options.endpoint_file

    endpoints = []
    try:
        with open(endpoint_file) as file:
            for endpoint in file:
                endpoints.append(endpoint)
    except FileNotFoundError:
        print('File was not found')
        sys.exit(1)

    if len(endpoints) == 0:
        print('File is empty')
        sys.exit(1)

    for endpoint in endpoints:
        print('Comments on ' + endpoint + '\n-------------')
        res = requests.get(base_url + endpoint)
        soup = bs4.BeautifulSoup(res.content, 'html.parser')
        comments = soup.find_all(text=is_comment)
        for com in comments:
            print(com.extract() + '\n')
        print('-------------\n')
