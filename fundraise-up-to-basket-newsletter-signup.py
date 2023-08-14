#Zap: Fundraise Up to Basket Newsletter Signup

#Very sketch way of getting our localization subfolder from the source URL so that we can assign language to send to basket. It's a living.
#This will very much fall apart if the URL structure of fo.mo changes, we really need Fundraise Up to send the language code here or at least
#send custom variables that we set, because this is at best still wrong when user browser settings are different than the URL.
#input_data is a Zapier-specific dict injected into the environment, it holds the data from a previous step in the Zap.
#lang needs to be at least initialized as an empty string or Basket will kick everything back with an error
if input_data['source_url'].startswith("https://foundation.mozilla.org") or input_data['source_url'].startswith("https://donate.mozilla.org"):
    urlParts = input_data['source_url'].split("/")
    lang = urlParts[3]
else: 
    lang = ""

#Possibly foolish, but let's lean on the assumption that Fundraise Up has passed everything below in the correct format.
payload = {
    'email': input_data['email'],
    'format': 'html',
    'country': input_data['country'],
    'lang': lang,
    'newsletters': 'mozilla-foundation',
    'source_url': input_data['source_url']
}

try:
    response = requests.post('https://basket.mozilla.org/news/subscribe/', data=payload)
    response.raise_for_status()
except HTTPError as http_err:
        print(f'HTTP error: {http_err}')
except Exception as e:
        print(f'Error: {e}')
  
#output variable is once again Zapier-specific, Zapier will grab this and display on testing and help with error checking. This is essentially a return statement.
output = response.json()
