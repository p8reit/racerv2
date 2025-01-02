import uuid
import json
import logging
from datetime import datetime
from io import BytesIO
from PIL import Image

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.core.cache import cache

from .models import TrackedRequest, ConnectionRecord

logger = logging.getLogger(__name__)

# Cache the GIF to optimize responses
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
@permission_required('racerv2.change_trackedrequest', raise_exception=True)
def hide_group(request):
    if request.method == "POST":
        group_name_to_hide = request.POST.get("group_name_to_hide")
        if group_name_to_hide:
            TrackedRequest.objects.filter(group_name=group_name_to_hide).update(is_hidden=True)
    return render(request, 'racerv2/dashboard.html')

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

        # Whitelist specific headers to extract
        allowed_headers = [
            'HTTP_HOST', 'HTTP_USER_AGENT', 'HTTP_ACCEPT', 'HTTP_ACCEPT_LANGUAGE',
            'HTTP_ACCEPT_ENCODING', 'HTTP_COOKIE', 'HTTP_CONNECTION', 'HTTP_UPGRADE_INSECURE_REQUESTS',
            'HTTP_SEC_FETCH_SITE', 'HTTP_SEC_FETCH_MODE', 'HTTP_SEC_FETCH_USER', 'HTTP_SEC_FETCH_DEST'
        ]

        headers = {key: value for key, value in request.META.items() if key in allowed_headers}
        headers_json = json.dumps(headers)  # Serialize the filtered headers

        # Retrieve the tracked request
        tracked_request = TrackedRequest.objects.filter(unique_id=unique_id).first()
        if not tracked_request:
            logger.warning(f"Invalid unique_id accessed: {unique_id}")
            return HttpResponse("Invalid unique_id", status=404)

        # Save connection record (assuming ConnectionRecord is properly set up)
        ConnectionRecord.objects.create(
            tracked_request=tracked_request,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer,
            headers=headers_json,
            timestamp=timezone.now()
        )

        # Serve the 1x1 transparent GIF
        return HttpResponse(get_1x1_gif(), content_type='image/gif')
    except Exception as e:
        logger.error(f"Error processing request for {unique_id}: {str(e)}")
        return HttpResponse("Error processing the request", status=500)

@login_required
@permission_required('racerv2.view_trackedrequest', raise_exception=True)
def dashboard(request):
    logs = TrackedRequest.objects.filter(is_hidden=False).order_by('-timestamp')

    return render(request, 'racerv2/dashboard.html', {
        'logs': logs,
        'total_logs': logs.count(),
    })
