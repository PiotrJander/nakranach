from rest_framework.response import Response

from app.api.serializers import TapChangeSerializer

def tap_changes_response(queryset, request, default_count=5):
    count = request.GET.get('count', default_count)
    tap_changes = queryset.order_by('-timestamp')[:count]
    serializer = TapChangeSerializer(tap_changes, many=True, context={'request': request})
    return Response(serializer.data)