from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger('apps')

def custom_exception_handler(exc, context):
    """
    Custom DRF exception handler to ensure standard error response schema:
    {
        "status": "error",
        "message": "Human readable summary",
        "errors": details_or_dict
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            "status": "error",
            "message": "An error occurred while processing your request.",
            "errors": response.data
        }

        if isinstance(response.data, dict):
            if "detail" in response.data:
                custom_response_data["message"] = str(response.data["detail"])
                del response.data["detail"]
                custom_response_data["errors"] = response.data if response.data else None
            elif "non_field_errors" in response.data:
                custom_response_data["message"] = " ".join(response.data["non_field_errors"])

        response.data = custom_response_data
    else:
        logger.error(f"Unhandled Exception: {exc}", exc_info=True)
        return Response(
            {
                "status": "error",
                "message": "Internal Server Error",
                "errors": {"detail": str(exc)}
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
