import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def text_response(request):
    """
    Return a HttpResponse with a simple text message.
    Check that the default content type of the response must be "text/html".
    """
    return HttpResponse('text/html', content_type='text/html')


def looks_like_json_response(request):
    """
    Return a HttpResponse with a text message containing something that looks
    like a JSON document, but it's just "text/html".
    """
    json_like = {
        'key': 'value',
        'key2': 'value'
    }
    return HttpResponse(str(json_like), content_type='text/html')


def simple_json_response(request):
    """
    Return an actual JSON response by setting the `content_type` of the HttpResponse
    object manually.
    """
    json_like = json.dumps({
        'key': 'value',
        'key2': 'value'
    })
    
    return HttpResponse(json_like, content_type='application/json')


def json_response(request):
    """
    Return the same JSON document, but now using a JsonResponse instead.
    """
    json_like = {
        'key': 'value',
        'key2': 'value'
    }
    return JsonResponse(json_like)


def json_list_response(request):
    """
    Return a JsonReponse that contains a list of JSON documents
    instead of a single one.
    Note that you will need to pass an extra `safe=False` parameter to
    the JsonResponse object it order to avoid built-in validation.
    https://docs.djangoproject.com/en/2.0/ref/request-response/#jsonresponse-objects
    """
    json_list = [{
        'key1': 'value'
    },{
        'key2': 'value'
    }]
    
    return JsonResponse(json_list, safe=False)


def json_error_response(request):
    """
    Return a JsonResponse with an error message and 400 (Bad Request) status code.
    """
    json_like = {
        'key1': 'value'
    }
    
    return JsonResponse(json_like, status=400)


@csrf_exempt
def only_post_request(request):
    """
    Perform a request method check. If it's a POST request, return a message saying
    everything is OK, and the status code `200`. If it's a different request
    method, return a `400` response with an error message.
    """
    if request.method == 'POST':
        return HttpResponse('OK', status=200)
    return HttpResponse('post only my guy', status=400)


@csrf_exempt
def post_payload(request):
    """
    Write a view that only accepts POST requests, and processes the JSON
    payload available in `request.body` attribute.
    """
    if request.method == 'POST':
        data = request.body
        data = data.decode()
        data = json.loads(data)
        print(data)
        return JsonResponse({"status": "ok"}, status=201)
    return HttpResponse('post only my guy', status=400)


def custom_headers(request):
    """
    Return a JsonResponse and add a custom header to it.
    """
    response = JsonResponse({'status': 'ok'}, status=200)
    response['custom-header'] = 'ch_content'
    return response


def url_int_argument(request, first_arg):
    """
    Write a view that receives one integer parameter in the URL, and displays it
    in the response text.
    """
    return JsonResponse({'recieved': first_arg})


def url_str_argument(request, first_arg):
    """
    Write a view that receives one string parameter in the URL, and displays it
    in the response text.
    """
    return HttpResponse('Recieved: {}'.format(first_arg))


def url_multi_arguments(request, first_arg, second_arg):
    """
    Write a view that receives two parameters in the URL, and display them
    in the response text.
    """
    return HttpResponse('Recieved: {}, {}'.format(first_arg, second_arg))


def get_params(request):
    """
    Write a view that receives GET arguments and display them in the
    response text.
    """
    return JsonResponse(request.GET)
