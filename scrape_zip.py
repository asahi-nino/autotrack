import requests
from lxml import html

# Not sure about the values for this
USERNAME = "<USER NAME>"
PASSWORD = "<PASSWORD>"

LOGIN_URL = "https://www.zipgrade.com/login"
URL = "https://www.zipgrade.com/tags/"

def main():
    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]

    # Create payload
    payload = {
        "username": USERNAME, 
        "password": PASSWORD, 
        "csrfmiddlewaretoken": authenticity_token
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
    
    # validate results
    result.ok # Will tell us if the last request was ok
    result.status_code # Will give us the status from the last request

    # Scrape url
    result = session_requests.get(URL, headers = dict(referer = URL))
    
    # validate results
    result.ok # Will tell us if the last request was ok
    result.status_code # Will give us the status from the last request
    
    tree = html.fromstring(result.content)
    bucket_names = tree.xpath("//div[@class='repo-list--repo']/a/text()")

    print(bucket_names)

if __name__ == '__main__':
    main()
