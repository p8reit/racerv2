import uuid
import json
import logging
from datetime import datetime
from io import BytesIO
from PIL import Image
import uuid

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.core.cache import cache
from django.shortcuts import render


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


def generate_links_action(request):
    # Placeholder logic for the action
    return JsonResponse({"message": "This is the generate-links-action endpoint."})


@login_required
@permission_required('racerv2.view_trackedrequest', raise_exception=True)
def generate_links(request):
    if request.method == 'POST':
        try:
            # Get parameters from the request
            num_links = int(request.POST.get('num_links', 0))  # Default to 0 if not provided
            group_name = request.POST.get('group_name', 'Default Group')  # Default group name

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

            # Render the links in the UI for web requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"generated_links": generated_links})

            return render(request, 'racerv2/generate_links.html', {
                "generated_links": generated_links,
                "group_name": group_name
            })
        except (ValueError, KeyError) as e:
            return JsonResponse({"error": f"Invalid input: {str(e)}"}, status=400)
    
    # For GET requests, render the page with a form
    return render(request, 'racerv2/generate_links.html')

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
    # Fetch logs with related connection records
    logs = TrackedRequest.objects.filter(is_hidden=False).order_by('-timestamp')

    # Enrich logs with related connection records
    enriched_logs = []
    for log in logs:
        connection_records = ConnectionRecord.objects.filter(tracked_request=log).order_by('-timestamp')
        enriched_logs.append({
            'log': log,
            'connection_records': connection_records
        })

    # Calculate totals
    total_logs = logs.count()
    relay_count_total = sum(int(log.relay_count) for log in logs if str(log.relay_count).isdigit())
    google_hosted_count = sum(
        1
        for log in logs
        for record in ConnectionRecord.objects.filter(tracked_request=log)
        if record.is_google_hosted
    )

    return render(request, 'racerv2/dashboard.html', {
        'logs': enriched_logs,
        'total_logs': total_logs,
        'relay_count_total': relay_count_total,
        'google_hosted_count': google_hosted_count,
    })
