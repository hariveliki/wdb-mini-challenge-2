import requests, base64, json

class AkeneoAPIClient:

   def __init__(self, **kwargs):
      self.clientId = kwargs.get('clientId')
      self.password = kwargs.get('password')
      self.secret = kwargs.get('secret')
      self.username = kwargs.get('username')
      self.url = kwargs.get('url')
      self.access_token = None
      self.refresh_token = None

   
   def login_with_password(self):
      login_payload = {}
      login_payload['grant_type'] = 'password'
      login_payload['username'] = self.username
      login_payload['password'] = self.password
      self.session = requests.Session()
      headers = self.get_auth_headers(self.clientId, self.secret)
      auth_url = self.url + '/api/oauth/v1/token'
      response = self.session.post(auth_url, headers=headers, json=login_payload)
      response_json = self.parse_response(response)
      self.access_token = response_json['access_token']
      self.refresh_token = response_json['refresh_token']
   

   def get_auth_headers(self, client_id, secret):
      base64_authorization = self.get_base_64_encoded_auth(client_id, secret)
      headers = {}
      headers["Content-Type"] = "application/json"
      headers["Authorization"] = base64_authorization
      return headers
   

   def get_base_64_encoded_auth(self, client_id, secret):
      if not client_id or not secret:
         raise Exception("Cannot generate base64 encoded auth because at least one of them is None!")
      message = client_id + ":" + secret
      message_bytes = message.encode("ascii")
      base64_bytes = base64.b64encode(message_bytes)
      base64_message = "Basic " + base64_bytes.decode("ascii")
      return base64_message
   

   def get_auth_token_by_refresh_token(self):
      login_payload = {}
      login_payload["refresh_token"] = self.refresh_token
      login_payload["grant_type"] = "refresh_token"
      headers = self.get_auth_headers(self.client_id, self.secret)
      auth_url = self.base_url + "/api/oauth/v1/token"
      response = self.session.request("POST", auth_url, headers=headers, json=login_payload)
      response_json = self.parse_response(response)
      access_token = response_json["access_token"]
      refresh_token = response_json["refresh_token"]
      self.access_token = access_token
      self.refresh_token = refresh_token
      return access_token, refresh_token

   def parse_response(self, response):
      if response.status_code == 200:
         return response.json()
      else:
         raise Exception('Response code: ' + str(response.status_code) + ' ' + response.text)


   def get_all_pages_from_akeneo_request(self, client, client_method_name, search_query=None):
      method = getattr(client, client_method_name)
      if search_query:
         raw_products = method(search_query)
      else:
         raw_products = method()
      next_cursor_url = self.get_next_cursor_url(raw_products)
      products = self.get_items_from_response_body(raw_products)
      clean_products = self.remove_elements_from_items(products, ["_links"])
      while next_cursor_url:
         new_raw_products = self.get_following_cursor_items(url=next_cursor_url)
         next_cursor_url = self.get_next_cursor_url(new_raw_products)
         new_products = self.get_items_from_response_body(new_raw_products)
         new_clean_products = self.remove_elements_from_items(new_products, ["_links"])
         clean_products = clean_products + new_clean_products
      return clean_products


   def get_next_cursor_url(self, response_json):
      if not response_json:
         raise Exception("akeneo_utils.get_next_cursor_url reponse_json parameter is empty or None!")
      if "_links" in response_json:
         if "next" in response_json["_links"]:
               return response_json["_links"]["next"]["href"]
      return None


   def get_items_from_response_body(self, response_body):
      if not response_body or not "_embedded" in response_body:
         raise Exception("In akeneo_utils.get_items_from_response_body: invalid response body: " + str(response_body))
      return response_body["_embedded"]["items"]


   def remove_elements_from_items(self, items, elements = []):
      clean_items = []
      for old_item in items:
         item = dict(old_item)
         for element in elements:
               item.pop(element, None)
         clean_items.append(item)
      return clean_items


   def get_following_cursor_items(self, url):
      headers = {}
      headers["Authorization"] = "Bearer " + self.access_token
      response = self.send_request(http_method="GET", url=url, headers=headers)
      items = self.parse_response(response=response)
      return items


   def parse_response(self, response):
      try:
         response_content = response.json()
      except:
         response_content = response.content
      if response.status_code < 300:
         return response_content
      else:
         raise Exception("API returned the following error: {}".format(response_content))


   def get_products(self, search_filter=None):
      headers = {}
      headers["Authorization"] =  "Bearer " + self.access_token
      url = self.url + "/api/rest/v1/products"
      response = self.send_search_request(url=url, headers=headers, search_filter=search_filter)
      items = self.parse_response(response=response)
      return items


   def send_search_request(self, url, headers = {}, search_filter=None):
      if search_filter:
         params = {"search": json.dumps(search_filter),"pagination_type": "search_after","limit": 100}
         response = self.send_request("GET", url, headers, params, {})
      else:
         params = {"pagination_type": "search_after", "limit": 100}
         response = self.send_request("GET", url, headers, params, {})
      return response


   def send_request(self, http_method, url, headers = {}, params = {}, payload = {}):
      response = self.session.request(http_method, url, params=params, headers=headers, json=payload)
      if response.status_code != 401:
         return response
      else:
         self.get_auth_token_by_refresh_token()
         headers = {}
         headers["Authorization"] =  "Bearer " + self.access_token
         response = self.session.request(http_method, url, params=params, headers=headers, json=payload)
         return response
