import gevent
import requests
import time
import locust
from locust import HttpUser, task, constant

def async_success(name, start_time, resp):
    locust.events.request_success.fire(
        request_type=resp.request.method,
        name=name,
        response_time=int((time.monotonic() - start_time) * 1000),
        response_length=len(resp.content),
    )

def async_failure(name, start_time, resp, message):
    locust.events.request_failure.fire(
        request_type=resp.request.method,
        name=name,
        response_time=int((time.monotonic() - start_time) * 1000),
        exception=Exception(message),
    )

class reportService(HttpUser):

    wait_time = constant(1)

    def _do_async_thing_handler(self, timeout=600):
        post_resp = requests.post(self.host + 'report')
        if not post_resp.status_code == 200:
            return
        id = post_resp.json()['report_id']
        print(id)

        # Now poll for an ACTIVE status
        start_time = time.monotonic()
        end_time = start_time + timeout
        while time.monotonic() < end_time:
            r = requests.get(self.host + 'report/' + id)
            if r.status_code == 200 and r.json()['result'] != None:
                async_success('POST /report/ID - async', start_time, post_resp)
                return

            # IMPORTANT: Sleep must be monkey-patched by gevent (typical), or else
            # use gevent.sleep to avoid blocking the world.
            time.sleep(1)
        async_failure('POST /report/ID - async', start_time, post_resp,
                      'Failed - timed out after %s seconds' % timeout)

    @task
    def do_async_thing(self):
        gevent.spawn(self._do_async_thing_handler)