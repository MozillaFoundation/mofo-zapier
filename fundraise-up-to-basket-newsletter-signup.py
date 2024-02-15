#Zap: Fundraise Up to Basket Newsletter Signup

#Note: Zapier is limited to using plain old Python 3.8.
#Very sketch way of getting our localization subfolder from the source URL so that we can assign language to send to basket. It's a living.
#This will very much fall apart if the URL structure of fo.mo changes, we really need Fundraise Up to send the language code here or at least
#send custom variables that we set, because this is at best still wrong when user browser settings are different than the URL.
#input_data is a Zapier-specific dict injected into the environment, it holds the data from a previous step in the Zap.
#In the previous step of the zap the fields are mapped from Fundraise Up to the keys that are being used in input_data dict.
#lang needs to be at least initialized as an empty string or Basket will kick everything back with an error.
#Basket will default an empty lang string to an en or English subscription.


#First set the URLs that we want to look for
#UPDATE THIS WHEN REQUIRED
URL_STARTS = ["https://foundation.mozilla.org"
              ,"https://donate.mozilla.org"
              ,"https://donor.mozilla.org"]

#Iterate through the urls and check them against the source_url, if any there are any matches in the list then process the URL
if any([input_data['source_url'].startswith(u) for u in URL_STARTS]):
    urlParts = input_data['source_url'].split("/")
    lang = urlParts[3]

#If the URL isn't one of our expected ones then set the language to "" which will result in en
else:
     lang = ""

#Possibly foolish, but let's lean on the assumption that Fundraise Up has passed everything below in the correct format.
#Changing the assumption slightly and using get to retrieve the right key and value (or None). Since email is required force
#that to be checked before creating the payload. Only send the request if the email is populated.
if input_data.get('email'):
    payload = {
        'email': input_data.get('email'),
        'format': 'html',
        'country': input_data.get('country'),
        'lang': lang,
        'newsletters': 'mozilla-foundation',
        'source_url': input_data.get('source_url')
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

else:
    output = 'REQUEST NOT SENT, PAYLOAD INCOMPLETE'
