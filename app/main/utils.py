def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


def add_middleware_to_response(response, middleware_class):
    middleware = middleware_class()
    middleware.process_response(response)
    return response


def setup_view(view, request, *args, **kwargs):
    """
    Mimic as_view() returned callable, but returns view instance.
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs


def normalize_for_search(string):
    """
    Takes the brewery name and beer name, concatenates them, and makes sure words are separated by a single space.
    """
    return ' '.join(string.split()).lower()