from ds_caselaw_utils.courts import courts as courts_repository
from rest_framework import serializers, viewsets
from rest_framework.response import Response


class BodySerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:body-detail", lookup_field="code")
    name = serializers.CharField(read_only=True)
    type = serializers.CharField(source="type.value", read_only=True)
    code = serializers.CharField(read_only=True)
    canonical_param = serializers.CharField(read_only=True)
    params = serializers.ListField(child=serializers.CharField(read_only=True), source="param_aliases", read_only=True)


class RichBodySerializer(BodySerializer):
    """Let the bodies hit the floor"""

    link = serializers.CharField(read_only=True)
    description_html = serializers.CharField(source="description_text_as_html", read_only=True)


class BodiesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BodySerializer
    queryset = courts_repository.get_all()
    lookup_field = "code"

    def retrieve(self, request, code=None):
        serializer = RichBodySerializer(courts_repository.get_by_code(code), context={"request": request})
        return Response(serializer.data)
