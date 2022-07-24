import time
from first_job.models import ResponseLogs


class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        end = time.time()
        ResponseLogs.objects.create(
            status_code=response.status_code,
            path=request.path,
            response_time=(end - start) * 1_000

        )
        return response
