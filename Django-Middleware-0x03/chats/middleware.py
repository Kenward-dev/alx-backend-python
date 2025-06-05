import logging
from datetime import datetime

class RequestLoggingMiddleware:
    """
    Middleware to log user requests including timestamp, user, and request path.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request_logger')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            file_handler = logging.FileHandler('requests.log')
            formatter = logging.Formatter('%(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.email if hasattr(request.user, 'email') else str(request.user)
        else:
            user = "Anonymous"
        
        self.logger.info(
            f"{datetime.now()} - User: {user} - Path: {request.path}"
        )
        
        response = self.get_response(request)
        
        return response