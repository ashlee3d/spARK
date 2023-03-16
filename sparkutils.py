import requests
def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def list_to_string(list):
    string = ""
    for item in list:
        string += item + "\n"
    return string

def ctx_info(ctx):
    attrs = ['author', 'channel', 'guild', 'message', 'bot']
    output = ''
    for attr in attrs:
        value = getattr(ctx, attr, None)
        if value is not None:
            output += f'{attr}: {value}\n\n'
    return output
def get_random_wiki_image():
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnnamespace": 6,
        "rnlimit": 1,
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("query") and data["query"].get("random"):
        file_title = data["query"]["random"][0]["title"]
        direct_image_url = get_direct_image_url(file_title)
        return direct_image_url

    return None
def get_direct_image_url(file_title):
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "titles": file_title,
        "iiprop": "url",
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if "imageinfo" in page:
            return page["imageinfo"][0]["url"]
    
    return None