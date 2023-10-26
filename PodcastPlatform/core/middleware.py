from datetime import datetime
from elasticsearch import Elasticsearch

from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings
from datetime import datetime


class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.es = Elasticsearch('http://elastic:9200')
        # self.gl = GeoIP2()

    def __call__(self, request):
        ip_address = get_client_ip(request)

        log_data = {
            'timestamp': datetime.now(),
            'request_method': request.method,
            'request_path': request.path,
            'request_ip': ip_address,
            # 'request_country': self.gl.country(ip_address),
            # 'request_city': self.gl.city(ip_address),
            'request_user_agent': request.META.get('HTTP_USER_AGENT', 'null'),
            'event': "api_req",
        }

        response = self.get_response(request)
        
        if not request.META.get("exception", False):
            user = request.user if hasattr(request, "user") else None

            log_data['user'] = user.id if user else None
            log_data['status_code'] = response.status_code

            self.es.index(index=f'{settings.LOG_INDEX_PREFIX}_{datetime.now().strftime("%Y-%m-%d")}', document=log_data)

        return response

    def process_exception(self, request, exception):
        ip_address = get_client_ip(request)

        log_data = {
            'timestamp': datetime.now(),
            'request_method': request.method,
            'request_path': request.path,
            'request_ip': ip_address,
            # 'request_country': self.gl.country(ip_address),
            # 'request_city': self.gl.city(ip_address),
            'request_user_agent': request.META.get('HTTP_USER_AGENT', 'null'),
            'exception_type': exception.__class__.__name__,
            'exception_message': exception.message if hasattr(exception, "message") else str(exception),
            'event': "api_exc",
        }

        request.META["exception"] = True

        self.es.index(index=f'{settings.LOG_INDEX_PREFIX}_{datetime.now().strftime("%Y-%m-%d")}', document=log_data)



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
