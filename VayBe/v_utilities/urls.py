from django.urls import Resolver404, resolve


def route_exists(path)->bool:
    try:
        resolve(path)
        return True
    except Resolver404:
        return False