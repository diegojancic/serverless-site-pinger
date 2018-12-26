import os
import ping


ENV_VAR_PREFIX = 'PINGURL_'

def lambda_handler(context):

    """
    url_list = [
        {'name': 'SERVER1', 'url': 'http://site-url-1.com/ping'},
        {'name': 'SERVER2', 'url': 'http://site-url-2.com/ping?key=secure-key'}
    ]
    """
    url_list = get_ping_urls()
    #print(url_list)

    results = ping.fetch_all(url_list)
    print (results)


def get_ping_urls():
    # Check all env vars
    vars = [var for var in os.environ if var.startswith(ENV_VAR_PREFIX)]
    url_list = []
    for v in vars:
        url_list.append({
            'name': v[len(ENV_VAR_PREFIX):],
            'url': os.environ[v]
        })
    return url_list

if __name__ == '__main__':
    # Set sample URLS
    os.environ[ENV_VAR_PREFIX + "TestServer"] = 'http://localhost:5000/ping'
    os.environ[ENV_VAR_PREFIX + "SslError"] = 'https://expired.badssl.com/'

    lambda_handler(None)
