def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


def add_middleware_to_response(response, middleware_class):
    middleware = middleware_class()
    middleware.process_response(response)
    return response
