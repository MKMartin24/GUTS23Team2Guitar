from typing import Dict
from django.http import HttpRequest


def login_ctx(request: HttpRequest) -> Dict:
    return {
        'login' : request.COOKIES.get('login')
    }
