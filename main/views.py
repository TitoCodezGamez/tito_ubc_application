from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from .models import FormEntry, Response
from .views_password import password
import json


@csrf_exempt
def save_response(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        response_name = data.get('response_name')
        if not response_name:
            return JsonResponse({'status': 'error', 'msg': 'No response name'}, status=400)
        response, _ = Response.objects.get_or_create(name=response_name)
        FormEntry.objects.filter(response__isnull=True).update(response=response)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

def home(request):
    selected_response = request.GET.get('response')
    all_responses = list(Response.objects.values_list('name', flat=True).order_by('created'))

    # If not specified, try to load last edited from session
    if not selected_response:
        selected_response = request.session.get('last_edited_response', None)
    # If still not set, default to 'new'
    if not selected_response:
        selected_response = 'new'

    # Save the selected response in session for next time
    request.session['last_edited_response'] = selected_response

    if selected_response and selected_response != 'new':
        try:
            response_obj = Response.objects.get(name=selected_response)
            entries_qs = FormEntry.objects.filter(response=response_obj)
        except Response.DoesNotExist:
            entries_qs = FormEntry.objects.none()
    else:
        entries_qs = FormEntry.objects.filter(response__isnull=True)
    entries = {e.name: {'text': e.text, 'dropdown': e.dropdown} for e in entries_qs}
    activities = []
    for i in range(1, 6):
        desc = entries.get(f'activity_desc_{i}', {'text': ''})['text']
        dropdown = entries.get(f'activity_type_{i}', {'dropdown': ''})['dropdown']
        activities.append({'desc': desc, 'dropdown': dropdown})
    dark_mode = request.session.get('dark_mode', False)
    return render(request, 'main/home.html', {
        'entries': entries,
        'activities': activities,
        'all_responses': all_responses,
        'selected_response': selected_response,
        'dark_mode': dark_mode,
    })

@csrf_exempt
def toggle_dark_mode(request):
    if request.method == 'POST':
        current = request.session.get('dark_mode', False)
        request.session['dark_mode'] = not current
        return JsonResponse({'status': 'ok', 'dark_mode': not current})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def autosave(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		name = data.get('name')
		text = data.get('text', '')
		dropdown = data.get('dropdown', '')
		response_name = data.get('response_name')
		response_obj = None
		if response_name:
			response_obj, _ = Response.objects.get_or_create(name=response_name)
		obj, created = FormEntry.objects.update_or_create(
			name=name,
			response=response_obj,
			defaults={'text': text, 'dropdown': dropdown}
		)
		return JsonResponse({'status': 'ok'})
	return JsonResponse({'status': 'error'}, status=400)
