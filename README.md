# Serverless Site Pinger

Small Python script that pings own sites and posts returned metrics (in addition to site response time) to CloudWatch.

# Setup

1. Rename `zappa_settings.json.template` to `zappa_settings.json`
1. Edit `zappa_settings.json` and change:
  1. `[S3-BUCKET-NAME]` by an unique bucket name. For example: company-zappa-deployments
  1. The `aws_environment_variables` directionary for a list of servers. See below.
1. On a shell navigate to the project directory and run:
  1. `cd src`
  1. `virtualenv env`
  1. `source env/bin/activate` (Linux) or `env\Scripts\activate.bat` (Windows)
  1. `pip install -r requirements.txt`

# Settings Servers to Monitor

The list of servers is read from the environment variables. For each environment variable
starting like `PINGURL_`, one server will be monitored. For example, if you set the env vars
as follows:

```
export PINGURL_EXAMPLE=http://example.com/ping
export PINGURL_ANOTER-SERVER=http://another-server.com/ping
```

Then, those 2 servers will be pinged. Now, if those URLs return a text file as follows:

```
ErrorRate: 2.35
ActiveUsers: 531
```

Then, the following metrics will be sent to CloudWatch:

```
EXAMPLE.Latency = x.xxx
EXAMPLE.ErrorRate = 2.35
EXAMPLE.ActiveUsers = 531

ANOTHER-SERVER.Latency = x.xxx
ANOTHER-SERVER.ErrorRate = 2.35
ANOTHER-SERVER.ActiveUsers = 531
```

The first part of the metric (before the `.`), corresponds to the env var name (after the `PINGURL_` prefix). The latency metric is always sent, and is sent as 9999 if there's an error while making the request. Also, for each line returned, a new metric is created and sent to CloudWatch.

To monitor only the latency of the page and not analyze the response, the environment variable name must end with an exclamation mark (!). For example:

```
export PINGURL_SITENAME!=http://example.com/ping
```

By using `PINGURL_SITENAME!` (note it ends with !), the script will ping the site and only record the latency in CloudWatch.


# Monitored Servers

The site you want to monitor must have a page that returns the metrics to be posted.

For example, you can create a page `https://www.example.com/ping` that returns the metrics.
If you want to keep the metrics private, you secure it with a random key, such as `?key=...`

To test this script you can run the sample server as follows:
1. `cd sample-server`
1. `virtualenv env`
1. `source env\bin\activate` (Linux) or `env\Scripts\activate.bat` (Windows)
1. `pip install -r requirements.txt`
1. `flask run`


# Test Scripts

After executing the steps listed in the [Setup section](#setup), run:

`python app.py`

# License

MIT
