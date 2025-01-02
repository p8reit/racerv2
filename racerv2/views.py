import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from .models import TrackedRequest
import json
from datetime import datetime
from io import BytesIO
from PIL import Image
import logging
from django.utils import timezone




logger = logging.getLogger(__name__)

# Cache the GIF to optimize responses
from django.core.cache import cache

def get_1x1_gif():
    gif = cache.get('1x1_gif')
    if not gif:
        image = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        img_io = BytesIO()
        image.save(img_io, 'GIF')
        gif = img_io.getvalue()
        cache.set('1x1_gif', gif)
    return gif

@login_required
@permission_required('racerv2.view_trackedrequest', raise_exception=True)
def generate_links(request):
    if request.method == 'POST':
        try:
            num_links = int(request.POST.get('num_links'))
            group_name = request.POST.get('group_name')

            if num_links <= 0:
                return JsonResponse({"error": "Number of links must be greater than zero."}, status=400)

            generated_links = []
            base_url = request.build_absolute_uri('/')[:-1]

            for i in range(num_links):
                unique_id = f'link_{uuid.uuid4()}'
                tracked_request = TrackedRequest(
                    unique_id=unique_id,
                    group_name=group_name
                )
                tracked_request.save()
                generated_links.append(f"{base_url}/racerv2/track/{unique_id}.gif")

            return JsonResponse({"generated_links": generated_links})
        except ValueError:
            return JsonResponse({"error": "Invalid input."}, status=400)
    
    return render(request, 'racerv2/generate_links.html')

@login_required
@permission_required('racerv2.view_trackedrequest', raise_exception=True)
def track_embed(request, unique_id):
    try:
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = request.META.get('REMOTE_ADDR', '')
        referrer = request.META.get('HTTP_REFERER', '')

        # Filter `request.META` to include only JSON-serializable values
        headers = {k: v for k, v in request.META.items() if isinstance(v, (str, int, float, bool, list, dict, type(None)))}
        headers_json = json.dumps(headers)  # Serialize the filtered dictionary

        # Retrieve the tracked request from the database
        tracked_request = TrackedRequest.objects.filter(unique_id=unique_id).first()
        if not tracked_request:
            logger.warning(f"Invalid unique_id accessed: {unique_id}")
            return HttpResponse("Invalid unique_id", status=404)

        # Update the tracked request with the new data
        tracked_request.ip_address = ip_address
        tracked_request.user_agent = user_agent
        tracked_request.referrer = referrer
        tracked_request.headers = headers_json
        tracked_request.timestamp = timezone.now()
        tracked_request.save()

        # Serve the 1x1 transparent GIF
        return HttpResponse(get_1x1_gif(), content_type='image/gif')
    except Exception as e:
        logger.error(f"Error processing request for {unique_id}: {str(e)}")
        return HttpResponse("Error processing the request", status=500)


@login_required
@permission_required('racerv2.view_trackedrequest', raise_exception=True)
def dashboard(request):
    logs = TrackedRequest.objects.filter(hidden=False).order_by('unique_id')
    logs_list = [
        {
            "unique_id": log.unique_id,
            "ip_address": log.ip_address,
            "user_agent": log.user_agent,
            "referrer": log.referrer,
            "geolocation": json.loads(log.geolocation) if log.geolocation else None,
            "timestamp": log.timestamp,
            "hidden": log.hidden
        }
        for log in logs
    ]

    logger.debug(f"Logs passed to dashboard: {logs_list}")

    return render(request, 'racerv2/dashboard.html', {
        'logs': logs_list,
        'total_logs': len(logs_list),
        'unique_ips': len(set(log['ip_address'] for log in logs_list))
    })
