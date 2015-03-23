from rest_framework.response import Response

from app.api.serializers import TapChangeSerializer

def tap_changes_response(queryset, request, view):
    count = request.GET.get('count', 5)
    tap_changes = None

    pagination_enabled = view.paginator is not None

    if pagination_enabled:
        tap_changes = view.paginator.paginate_queryset(queryset, request, view=view)
    else:
        tap_changes = queryset.order_by('-timestamp')[:count]

    serializer = TapChangeSerializer(tap_changes, many=True, context={'request': request})

    if pagination_enabled:
        return view.paginator.get_paginated_response(serializer.data)

    return Response(serializer.data)