from ds_caselaw_utils.courts import courts as courts_repository
from rest_framework.response import Response
from rest_framework.views import APIView


class BodiesView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all bodies.
        """

        courts = [
            {
                "name": court.name,
                "code": court.code,
                "canonical_param": court.canonical_param,
                "params": court.param_aliases,
            }
            for court in courts_repository.get_all()
        ]

        return Response(courts)
