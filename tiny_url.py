try: 
    from urllib.parse import urlencode           
except ImportError: 
    from urllib import urlencode 
  

import requests
  
def short_url(url):
    response = requests.get('https://tinyurl.com/api-create.php?' + urlencode({'url':url}))
    return(response.text)