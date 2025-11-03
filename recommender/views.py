from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from datetime import datetime, timezone
from .ai_agent import recommend_title_artist


def iso_now_z():
    """Return current UTC time in ISO 8601 with 'Z' suffix."""
    return datetime.utcnow().replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


@csrf_exempt
def music_agent_view(request):
    """
    A2A-compatible view that accepts JSON with a 'message' or 'query' field
    and returns the full Telex-style response structure.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        message = data.get("message") or data.get("query") or ""
        result = recommend_title_artist(message)

        # IDs and timestamp
        result_id = str(uuid.uuid4())
        message_id = str(uuid.uuid4())
        task_id = result_id
        artifact_id = str(uuid.uuid4())
        timestamp = iso_now_z()

        # Build the response
        response = {
            "jsonrpc": "2.0",
            "id": result_id,
            "result": {
                "id": result_id,
                "status": {
                    "state": "completed",
                    "timestamp": timestamp,
                    "message": {
                        "kind": "message",
                        "role": "agent",
                        "parts": [
                            {
                                "kind": "text",
                                "text": f"🎵 *{result['title']}* by {result['artist']}"
                            }
                        ],
                        "messageId": message_id,
                        "taskId": task_id
                    }
                },
                "artifacts": [
                    {
                        "artifactId": artifact_id,
                        "name": "music_recommendation",
                        "parts": [
                            {
                                "kind": "text",
                                "text": f"{result['title']} — {result['artist']}"
                            }
                        ]
                    }
                ],
                "kind": "task"
            }
        }

        return JsonResponse(response, safe=False, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


