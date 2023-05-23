import requests
import re
from bs4 import BeautifulSoup
from langchain.text_splitter import CharacterTextSplitter



def get_helius_links():
    helius_links = []
    r = requests.get('https://docs.helius.xyz/')
    soup = BeautifulSoup(r.text, 'html.parser')
    # Find all 'a' tags within divs with class 'css-175oi2r'
    links = soup.select('div.css-175oi2r a')
    for link in links:
        href = link.get('href')
        if href and href.startswith('/'):
            helius_links.append(href)
    # Remove duplicates and sort
    helius_links = sorted(list(set(helius_links)))
    return helius_links



def get_helius_info(extension):
    url = 'https://docs.helius.xyz' + extension
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # Get the div with the data-testid
    contents = soup.find('div', {'data-testid': 'page.contentEditor'})
    # Try to get the text
    try:
        contents = re.sub('(?<=[.!?])(?=[^\s])','\n', contents.text)
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=100, chunk_overlap=0)
        contents = text_splitter.split_text(contents)
        for text in contents:
            print(text)
            print()
    except:
        contents = ''
    return contents

links = get_helius_links()

# Create dictionaries in this formate: {'source': 'helius', 'title': 'title', 'description': 'description', 'link': 'link'}

base_dict = {'source': 'helius', 'title': '', 'content': '', 'link': ''}
final_json = []

for link in links:
    for content in get_helius_info(link):
        base_dict = {}  # Create a new dictionary in each iteration
        base_dict['link'] = 'https://docs.helius.xyz' + link
        base_dict['title'] = link.split('/')[-1]
        base_dict['type'] = 'content'
        base_dict['content'] = content
        final_json.append(base_dict)



# # Save the final_json to a json file
import json
with open('src/data_ingestion/helius/helius.json', 'w') as f:
    json.dump(final_json, f, indent=4)

