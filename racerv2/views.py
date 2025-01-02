from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, permission_required
from .models import TrackedRequest
import json
from datetime import datetime
from io import BytesIO
from PIL import Image
import logging

logger = logging.getLogger(__name__)

@login_required
@permission_required('embed_racing.view_trackedrequest', raise_exception=True)
def generate_links(request):
    if request.method == 'POST':
        num_links = int(request.POST.get('num_links'))
        group_name = request.POST.get('group_name')
        
        generated_links = []
        base_url = request.build_absolute_uri('/')[:-1]  # Get the base URL
        
        for i in range(num_links):
            unique_id = f'link_{int(datetime.now().timestamp())}_{i}'
            tracked_request = TrackedRequest(
                unique_id=unique_id,
                group_name=group_name
            )
            tracked_request.save()
            generated_links.append(f"{base_url}/embed_racing/track/{unique_id}.gif")
        
        return JsonResponse({"generated_links": generated_links})
    
    return render(request, 'embed_racing/generate_links.html')

@login_required
@permission_required('embed_racing.view_trackedrequest', raise_exception=True)
def track_embed(request, unique_id):
    try:
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = request.META.get('REMOTE_ADDR', '')
        referrer = request.META.get('HTTP_REFERER', '')
        headers = json.dumps(dict(request.META))
        
        tracked_request = TrackedRequest.objects.filter(unique_id=unique_id).first()
        if not tracked_request:
            logger.error(f"No initial request found for unique_id {unique_id}")
            return HttpResponse("Invalid unique_id", status=404)

        tracked_request.ip_address = ip_address
        tracked_request.user_agent = user_agent
        tracked_request.referrer = referrer
        tracked_request.headers = headers
        tracked_request.timestamp = datetime.now()
        tracked_request.save()

        # Create the 1x1 GIF image
        image = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        img_io = BytesIO()
        image.save(img_io, 'GIF')
        img_io.seek(0)
        
        return HttpResponse(img_io, content_type='image/gif')
    except Exception as e:
        logger.error(f"Error processing request for {unique_id}: {str(e)}")
        return HttpResponse("Error processing the request", status=500)

@login_required
@permission_required('embed_racing.view_trackedrequest', raise_exception=True)
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

    # Render the dashboard
    return render(request, 'embed_racing/dashboard.html', {
        'logs': logs_list,
        'total_logs': len(logs_list),
        'unique_ips': len(set(log['ip_address'] for log in logs_list))
    })
