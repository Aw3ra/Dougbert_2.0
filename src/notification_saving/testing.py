import requests
import json

url = "https://twttrapi.p.rapidapi.com/search-users"

querystring = {"query":"(to:@dougbertai) until:2023-05-20 since:2023-05-19"}

headers = {
	"twttr-session": "H4sIAKpLZGQC/42RS3ObMBRGgx+4XsTDQIE4tlPz8iPJghESBmLjvyJA0hXTbDxkSf97je2ZetGZVistvnPud+e+NnnoB+kkyDN8bH6eGgq0EBxKAKirEmjNoDXnS50YG3UtyYtwrWGWb9ZAV4NN3p/xdfPrdC+ZuBh5OOhcSrbKkGqERsRUeB6ZMTJ7VjV2hGLtntIynfqOESp4jF4MJDtNRi7cPn1GpGbBSBnojj6KrKeVhOVMG6Z9+TEaOIqpDb/TpeiQbnDuJW9hkOSXBQwcetg7aX979vhNW12/86m+dXDPtGi8+LGI0xGuieDpATL+VZr9wdzmW+1h4UbYSIe9vqcnD84s2OaWijdTz4xYgKsPx3Iz1bTVurK7LgSvE4QnCel62DrTmTRrG6hWQnnZDx0SfAwmvn+NFJxCKYhoMStQy1Ep2ppx2QJhvJAlRVUo7rCQXDFKo4pV0TlMCtryAsk2CkXd7jjsSLmrUB1Ch8U+doP7y7IahBBMFozyEgpeXOR5niX4HHi9Adcha/pVahRqXknOQBYFSAZQ/fEm5FzI/d/oPvQyHCTH+B+Agz03P4aH20FvZR7PyKRQlMj3Z0H2TWKkQk/d7YM4/vx8bJr3998sQLDkyAIAAA==",
	"X-RapidAPI-Key": "2665401a98mshb4ff8c9c9dc53efp1568abjsn0ce6e816b0c1",
	"X-RapidAPI-Host": "twttrapi.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring, stream=True)
print(response.text)
# with open('response.txt', 'w') as f:
#     f.write(response.text)

