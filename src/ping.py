
import threading
#from urllib.request import urlopen
import certifi
import urllib3
import time

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where(),
    timeout=20.0)

def fetch_url(name, url, results):
    start = time.time()

    # Make the request
    try:
        response = http.request('GET', url)
    except Exception as e:
        print('ERROR: Unable to fetch URL for {name} ({url}). Details: {error}'.format(name=name, url=url, error=str(e)))
        results.append({
                        'metric': name + ".Latency",
                        'value': 9999.0
                    })
        return

    response_text = response.data.decode('utf-8')
    # Add latency
    results.append({
                    'metric': name + ".Latency",
                    'value': time.time() - start
                })

    # remove empty lines (filter); remove \n from the end (strip); convert to list
    lines = list(map(str.strip, filter(None, response_text.split("\n"))))
    metrics = list(map(lambda l: l.split(':'), lines))

    try:
        for m in metrics:
            results.append({
                            'metric': name + "." + m[0],
                            'value': float(m[1].strip())
                        })
    except:
        print ('ERROR: Unable to parse received output. Output: {output}'.format(output=response_text))


def fetch_all(url_list):
    """
    url_list = [
        {'name': 'SERVER1', 'url': 'http://site-url-1.com/ping'},
        {'name': 'SERVER2', 'url': 'http://site-url-2.com/ping?key=secure-key'}
    ]
    """
    results = []

    threads = [threading.Thread(target=fetch_url, args=(url["name"], url["url"], results))
                    for url in url_list]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    #print ("Elapsed Time: %s" % (time.time() - start))
    return results
