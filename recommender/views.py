from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from datetime import datetime, timezone
from .ai_agent import recommend_title_artist


def iso_now_z():
    """Return current UTC time in ISO 8601 with 'Z' suffix."""
    return datetime.utcnow().replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def extract_user_message(data: dict) -> str:
    """
    Extract the user query text from various possible payload formats.
    Supports:
    - Simple {"message": "..."}
    - A2A {"params": {"message": {"parts": [...]}}}
    """
    # Direct message or query
    if "message" in data and isinstance(data["message"], str):
        return data["message"]

    # Telex-style A2A request
    try:
        parts = data["params"]["message"].get("parts", [])
        texts = []

        for part in parts:
            if part.get("kind") == "text" and part.get("text"):
                texts.append(part["text"])
            elif part.get("kind") == "data":
                for d in part.get("data", []):
                    if d.get("kind") == "text" and d.get("text"):
                        texts.append(d["text"])

        if texts:
            return " ".join(texts)
    except Exception:
        pass

    return data.get("query", "") or ""


@csrf_exempt
def music_agent_view(request):
    """
    A2A-compatible view that accepts JSON with a 'message' or 'query' field
    or Telex-style payload and returns the full response structure.
    """
    # Allow GET for Telex endpoint validation
    if request.method == "GET":
        return JsonResponse({
            "status": "ok",
            "message": "Music agent endpoint is active and ready."
        }, status=200)

    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        message = extract_user_message(data).strip()

        if not message:
            return JsonResponse({"error": "No message provided"}, status=400)

        result = recommend_title_artist(message)

        # IDs and timestamp
        task_id = f"task-{uuid.uuid4()}"
        message_id = f"msg-{uuid.uuid4()}"
        context_id = f"ctx-{uuid.uuid4()}"
        artifact_id = f"artifact-{uuid.uuid4()}"
        timestamp = iso_now_z()

        # Build the response (same as before)
        response = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "result": {
                "id": task_id,
                "contextId": context_id,
                "status": {
                    "state": "completed",
                    "timestamp": timestamp,
                    "message": {
                        "kind": "message",
                        "role": "agent",
                        "parts": [
                            {
                                "kind": "text",
                                "text": f"🎵 *{result['title']}* by {result['artist']}",
                                "data": None,
                                "file_url": None
                            }
                        ],
                        "messageId": message_id,
                        "taskId": task_id,
                        "metadata": None
                    }
                },
                "artifacts": [
                    {
                        "artifactId": artifact_id,
                        "name": "music_recommendation",
                        "parts": [
                            {
                                "kind": "text",
                                "text": f"{result['title']} — {result['artist']}",
                                "data": None,
                                "file_url": None
                            }
                        ]
                    }
                ],
                "history": [
                    {
                        "kind": "message",
                        "role": "user",
                        "parts": [
                            {
                                "kind": "text",
                                "text": message,
                                "data": None,
                                "file_url": None
                            }
                        ],
                        "messageId": f"msg-{uuid.uuid4()}",
                        "taskId": None,
                        "metadata": None
                    },
                    {
                        "kind": "message",
                        "role": "agent",
                        "parts": [
                            {
                                "kind": "text",
                                "text": f"🎵 *{result['title']}* by {result['artist']}",
                                "data": None,
                                "file_url": None
                            }
                        ],
                        "messageId": message_id,
                        "taskId": task_id,
                        "metadata": None
                    }
                ],
                "kind": "task"
            },
            "error": None
        }

        return JsonResponse(response, safe=False, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
