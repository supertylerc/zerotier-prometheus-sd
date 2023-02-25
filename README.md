# zerotier-prometheus-sd

`zerotier-prometheus-sd` is an async Prometheus HTTP Service Discovery
API server.  It has a single API endpoint that requires two parameters.
It is an ASGI application.  You can install and run it with:

```bash
$ poetry install

<snip>
$ poetry run uvicorn zerotier_prometheus_sd.app:app
INFO:     Will watch for changes in these directories: ['/home/tyler/Projects/github.com/supertylerc/zerotier-prometheus-sd']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [71268] using StatReload
INFO:     Started server process [71371]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Then, you can hit the endpoint with something like:

```bash
$ export ZT_API_KEY="example-api-key"
$ curl http://127.0.0.8000/zerotier_targets\?port\=9300\&network_id=abcdefg"
{"targets": ["192.0.2.1:9300", "192.0.2.100:9300"], "labels": {}}
```

Configure a Prometheus HTTP SD config and match the `port` and
`network_id` to your requirements, and Prometheus will scrape all of
ZeroTier systems on the port specified.

## Future

Right now, no labels are returned, and there's no way to filter the
members.  This serves my needs well enough for now, but in the future
additional labeling and filtering features may be added.

Tests exists and _technically_ cover every line of code, but that
doesn't mean the tests are exhaustive.  Testing might be improved in
the future, especially integration testing.

This needs to be published to PyPI.
