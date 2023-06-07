

def create_akeneo_api_client(credentials, AkeneoAPIClient):
    client = AkeneoAPIClient(
        clientId=credentials['clientId'],
        password=credentials['password'],
        secret=credentials['secret'],
        username=credentials['username'],
        url=credentials['url']
    )
    return client