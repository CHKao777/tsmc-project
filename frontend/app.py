
from flask import Flask
from redis import Redis
import rq_dashboard

app = Flask(__name__)
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")
app.config['RQ_DASHBOARD_REDIS_URL'] = 'redis://redis:6379'

cache = Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():   
    count = get_hit_count()
    return 'Hellos : {} {}'.format(count, app.config)