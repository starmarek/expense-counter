from django.apps import apps
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def validation_view(request):
    query = request.query_params

    model = apps.get_model(query["app"], query["model"])
    obj = model.objects.filter(**{query["field"]: query["value"]})
    return Response({"match": True if len(obj) > 0 else False}, status=200)
