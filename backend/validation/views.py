from django.apps import apps
from django.core.exceptions import FieldError
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def validation_view(request):
    required_queries = ["app", "model", "field", "value"]
    query = request.query_params
    if not all(req in query for req in required_queries):
        return Response(f"{required_queries} are required query param", status=400)

    try:
        model = apps.get_model(query["app"], query["model"])
    except LookupError:
        return Response("Couldn't find requested app or model", status=400)

    try:
        obj = model.objects.filter(**{query["field"]: query["value"]})
    except FieldError:
        return Response(f"Field '{query['field']}' don't exist in '{query['model']}' model", status=400)

    return Response({"match": True if len(obj) > 0 else False}, status=200)
