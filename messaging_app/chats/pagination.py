from rest_framework.pagination import PageNumberPagination

class MessagesPagination(PageNumberPagination):
    """
    Custom pagination class for the messaging app.
    
    This class extends the default PageNumberPagination to provide a custom page size
    and query parameter for page size.
    """
    page_size = 20  
    page_size_query_param = 'page_size'  
    max_page_size = 100 