import os
import boto3
import ping


ENV_VAR_PREFIX = 'PINGURL_'
cloudwatch = boto3.client('cloudwatch')


def lambda_handler(context):

    """
    url_list = [
        {'name': 'SERVER1', 'url': 'http://site-url-1.com/ping', options: {latencyOnly: true}},
        {'name': 'SERVER2', 'url': 'http://site-url-2.com/ping?key=secure-key', options: {latencyOnly: false}}
    ]
    """
    url_list = get_ping_urls()
    #print(url_list)

    results = ping.fetch_all(url_list)
    print (results)

    # Post metrics to CloudWatch
    post_to_cw(results)


def post_to_cw(results):
    """
    SAMPLE results:
    [{'metric': 'TESTSERVER.Latency', 'value': 1.2175002098083496},
    {'metric': 'TESTSERVER.ErrorRate', 'value': 2.35},
    {'metric': 'TESTSERVER.ActiveUsers', 'value': 531.0},
    {'metric': 'SSLERROR.Latency', 'value': 9999.0}]
    """

    cwdata = []
    for res in results:
        metric_unit = 'Seconds' if '.Latency' in res['metric'] else 'None'
        metric_parts = res["metric"].split('.')
        site_name = metric_parts[0]
        metric_name = metric_parts[1]

        cwdata.append({
            'MetricName': metric_name,
            'Dimensions': [
                {
                    'Name': 'Site',
                    'Value': site_name
                },
            ],
            'Unit': metric_unit,
            'Value': res['value']
        })

    cloudwatch.put_metric_data(
        MetricData=cwdata,
        Namespace='SiteMonitoring'
    )


def get_ping_urls():
    # Check all env vars
    vars = [var for var in os.environ if var.startswith(ENV_VAR_PREFIX)]
    url_list = []
    for v in vars:
        name = v[len(ENV_VAR_PREFIX):]
        options = {
            'latencyOnly': name[-1:] == '!'
        }
        if options['latencyOnly']:
            name = name[:-1]
        url_list.append({
            'name': v[len(ENV_VAR_PREFIX):],
            'url': os.environ[v],
            'options': options
        })
    return url_list

if __name__ == '__main__':
    # Set sample URLS
    os.environ[ENV_VAR_PREFIX + "TestServer"] = 'http://localhost:5000/ping'
    os.environ[ENV_VAR_PREFIX + "TestServerBadResp"] = 'http://localhost:5000/ping-bad-response'
    os.environ[ENV_VAR_PREFIX + "SslError"] = 'https://expired.badssl.com/'

    lambda_handler(None)
