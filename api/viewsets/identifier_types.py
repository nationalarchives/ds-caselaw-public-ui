from caselawclient.models.identifiers.unpacker import IDENTIFIER_NAMESPACE_MAP
from rest_framework import serializers, viewsets
from rest_framework.response import Response


class IdentifierTypeSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:identifier_type-detail", lookup_field="namespace")
    name = serializers.CharField(read_only=True)
    namespace = serializers.CharField(read_only=True)


class IdentifierTypesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IdentifierTypeSerializer
    queryset = [identifier_class.schema for identifier_class in IDENTIFIER_NAMESPACE_MAP.values()]
    lookup_field = "namespace"

    def retrieve(self, request, namespace=None):
        serializer = IdentifierTypeSerializer(IDENTIFIER_NAMESPACE_MAP[namespace].schema, context={"request": request})
        return Response(serializer.data)
