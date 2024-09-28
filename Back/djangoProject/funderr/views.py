from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    response_data = {
        "status": "success",
        "message": "Welcome to the API!",
        "data": {
            "name": "Django-Vue/Angular Integration",
            "version": "1.0",
            "description": "This is a sample JSON response from the Django server.",
            "features": [
                "REST API",
                "CORS Enabled",
                "Frontend Integration with Vue/Angular"
            ],
            "contact": {
                "email": "admin@example.com",
                "support": "http://example.com/support"
            }
        }
    }
    return JsonResponse(response_data)