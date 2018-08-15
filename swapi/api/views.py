import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import Planet, People
from api.fixtures import SINGLE_PEOPLE_OBJECT, PEOPLE_OBJECTS
from api.serializers import serialize_people_as_json


def single_people(request):
    return JsonResponse(SINGLE_PEOPLE_OBJECT)


def list_people(request):
    return JsonResponse(PEOPLE_OBJECTS, safe=False)


@csrf_exempt
def people_list_view(request):
    """
    People `list` actions:

    Based on the request method, perform the following actions:

        * GET: Return the list of all `People` objects in the database.

        * POST: Create a new `People` object using the submitted JSON payload.

    Make sure you add at least these validations:

        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """
    if request.method == 'GET':
        people = People.objects.all()
        people = [serialize_people_as_json(person) for person in people]
        
        '''method below also works'''
        # people = People.objects.all().values()
        # people = list(people)
        
        return JsonResponse(people, safe=False)
        
    elif request.method == 'POST':
        data = request.body
        if type(data) == bytes:
            data = data.decode()
        
        try:
            data = json.loads(data)
        except:
            return JsonResponse({'msg': 'Provide a valid JSON payload', 'success': False}, 400)
        
        try:
            planet = Planet.objects.get(id=data['homeworld'])
        except Planet.DoesNotExist:
            error_response = {
                "success": False,
                "msg": "Could not find planet  with id: {}".format(data['homeworld'])
            }
            return JsonResponse(error_response, status=404)
            
        if (type(data['height']) != int) or (type(data['mass']) != int):
                
                print(type(data['height']))
                print(type(data['mass']))
                print(data['hair_color'])
                
                return JsonResponse({
                    "success": False,
                    "msg": "Provided payload is not valid"
                }, status=400)
            
        new_person = People.objects.create(
            name=data['name'],
            height=data['height'],
            mass=data['mass'],
            homeworld=planet,
            hair_color=data['hair_color']
        )

        return JsonResponse(serialize_people_as_json(new_person), status=201)
    
    return JsonResponse({'msg': 'Invalid HTTP method', 'success': False}, status=400)


@csrf_exempt
def people_detail_view(request, people_id):
    """
    People `detail` actions:

    Based on the request method, perform the following actions:

        * GET: Returns the `People` object with given `people_id`.

        * PUT/PATCH: Updates the `People` object either partially (PATCH)
          or completely (PUT) using the submitted JSON payload.

        * DELETE: Deletes `People` object with given `people_id`.

    Make sure you add at least these validations:

        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """
    
    person = get_object_or_404(People, id=people_id)
    
    if request.method == "GET":
        return JsonResponse(serialize_people_as_json(person))
        
    elif request.method == "DELETE":
        person.delete()
        return JsonResponse({'success': True}, status=200)
        
    elif request.method == 'PATCH' or request.method == 'PUT':
        
        
        '''testing that request.body can be loaded as json'''
        try:
            data = request.body
            if type(data) == bytes:
                data = data.decode()
            data = json.loads(data)
        except:
            return JsonResponse({
                'msg': 'Provide a valid JSON payload', 
                'success': False
            }, status=400)    
        
        
        '''testing if a homeworld id is provided 
            and getting corresponding Planet'''
        planet = None    
        if data['homeworld']:
            try:
                planet = Planet.objects.get(id=data['homeworld'])
            except Planet.DoesNotExist:
                error_response = {
                    "success": False,
                    "msg": "Could not find planet  with id: {}".format(data['homeworld'])
                }
                return JsonResponse(error_response, status=404)
        
        
        '''testing validity of fields before updating'''
        if ((data['height'] and type(data['height']) != int)
            or (data['mass'] and type(data['mass']) != int)):
                
                return JsonResponse({
                    "success": False,
                    "msg": "Provided payload is not valid"
                }, status=400)
        
        
        '''testing all fields present for full update'''
        if (request.method == 'PUT') and not (len(data) == 5):
            return JsonResponse({
                'msg': 'Missing field in full update', 
                'success': False}, status=400)
        
        
        '''reassigning each attribute if provided, else leaving the same'''    
        person.name = data['name'] or person.name
        person.height = data['height'] or person.height
        person.mass = data['mass'] or person.mass
        person.homeworld = planet or person.homeworld
        person.hair_color = data['hair_color'] or person.hair_color
        person.save()
        
        return JsonResponse({'Success': True}, status=200)
    
    return JsonResponse({'msg': 'Invalid HTTP method', 'success': False}, status=400)