import logging
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response

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

class RestrictAccessByTimeMiddleware:
    """
    Custom middleware to restrict access to the application based on time.
    Access is allowed only between 9 PM (21:00) and 6 AM (06:00).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        
        if current_hour >= 21 or current_hour < 6:
            return self.get_response(request)
        else:
            return self._deny_access()

    def _deny_access(self):
        """
        Return a 403 Forbidden response when access is denied.
        """
        return Response(
            "Access is restricted to (9 PM - 6 AM).",
            status=status.HTTP_403_FORBIDDEN
        )