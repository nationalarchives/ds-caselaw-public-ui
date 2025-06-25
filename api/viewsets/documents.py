from caselawclient.client_helpers.search_helpers import search_judgments_and_parse_response
from caselawclient.search_parameters import SearchParameters
from rest_framework import filters, serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter,OpenApiTypes
from judgments.converters import DOCUMENT_URI_REGEX_PATTERN
from judgments.utils import api_client, get_published_document_by_uri


class DocumentSearchResultSerialiser(serializers.Serializer):
    self = serializers.HyperlinkedIdentityField(view_name="api:document-detail", lookup_field="uri")
    uri = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)


class SearchAsQuerysetFacade:
    def __init__(self, search_params: SearchParameters):
        self.search_params = search_params

    def __len__(self):
        return search_judgments_and_parse_response(api_client, self.search_params).total

    def __getitem__(self, index):
        if isinstance(index, slice):
            self.search_params.page_size = index.stop - index.start
            self.search_params.page = (index.start / self.search_params.page_size) + 1
        else:
            self.search_params.page_size = 1
            self.search_params.page = index + 1

        return search_judgments_and_parse_response(api_client, self.search_params).results

    def set_search_param(self, param, value):
        self.search_params.__setattr__(param, value)


class DocumentsViewPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100


class DocumentSearchFilterBackend(filters.BaseFilterBackend):
    """Filter to apply a MarkLogic search query."""

    def filter_queryset(self, request, queryset, view):
        queryset.set_search_param("query", request.query_params.get("query"))
        return queryset

@extend_schema_view(
    list=extend_schema(
        parameters=[
          OpenApiParameter("query", OpenApiTypes.STR, OpenApiParameter.QUERY, description="The search term."),
        ]
    )
)
class DocumentsViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = DocumentsViewPagination
    serializer_class = DocumentSearchResultSerialiser
    filter_backends = [DocumentSearchFilterBackend]
    lookup_field = "uri"
    lookup_value_regex = DOCUMENT_URI_REGEX_PATTERN
    queryset = SearchAsQuerysetFacade(SearchParameters())

    def retrieve(self, request, uri=None):
        serializer = DocumentSearchResultSerialiser(get_published_document_by_uri(uri), context={"request": request})
        return Response(serializer.data)
