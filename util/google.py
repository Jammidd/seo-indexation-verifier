import requests

def sanitize(url):
    url = url.replace("www.", "")
    url = url.replace(" ", "")
    url = url.strip()
    return url

def is_indexed_by_google(url):
    CUSTOM_SEARCH_URL = 'https://www.googleapis.com/customsearch/v1/siterestrict?'

    api_key = API_KEY
    api_cx = API_CONTEXT_CX
    api_url = "{}key={}&cx={}&q={}".format(CUSTOM_SEARCH_URL, api_key, api_cx, url)

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if int(data["searchInformation"]["totalResults"]) > 0:
            indexed_url = [item for item in data["items"] if sanitize(item["formattedUrl"]) == url]

            if len(indexed_url) > 0:
                return True

    return False