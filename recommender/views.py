from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .ai_agent import recommend_title_artist

@csrf_exempt
def music_agent_view(request):
    """
    A2A-compatible view that accepts JSON with a 'message' or 'query' field
    and returns { "title": ..., "artist": ... }.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        message = data.get("message") or data.get("query") or ""
        result = recommend_title_artist(message)

        # A2A-compatible format
        return JsonResponse({
            "response": result,
            "status": "success"
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

