from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, ctx):
    response = exception_handler(exc, ctx)

    if response is None:
        return Response(
            {"error": "Internal Server Error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    response.data = {
        "error": response.data.get("detail", "An error occured"),
        "status_code": response.status_code,
    }

    return response
