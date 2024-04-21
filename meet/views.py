from django.shortcuts import render
from django.views import View
from database.models import Meet
from django.http import JsonResponse
import json

class MeetHandler(View):
    def get(self, request, id=None):
        # This method will get all the meetings from the database and return them as a JSON response.
        if id is not None:
            meet_data = Meet.objects.filter(id=id, is_deleted=False).values()
        else:
            meet_data = Meet.objects.filter(is_deleted=False).values()
        if meet_data is None:
            response = {'message': 'Meeting not found'}
            return JsonResponse(response)
        meet_data_json = list()
        for meet in meet_data:
            meet_data_json.append({
                'id': meet['id'],
                'date': meet['date'].strftime('%Y-%m-%d'),
                'start_hour': meet['start_hour'].strftime('%H:%M:%S'),
                'end_hour': meet['end_hour'].strftime('%H:%M:%S'),
                'description': meet['description'],
                'participants': meet['participants']
            })
        return JsonResponse(meet_data_json, safe=False)
    
    def post(self, request):
        # This method will create a new meeting in the database.
        meet_data = json.loads(request.body)
        date = meet_data.get('date')
        start_hour = meet_data.get('start_hour')
        end_hour = meet_data.get('end_hour')
        description = meet_data.get('description')
        participants = meet_data.get('participants')
        response = {'success': False}
    
        if date is None or start_hour is None or end_hour is None or description is None or participants is None:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'})
        
        print(date, start_hour, end_hour, description, participants)
        Meet.objects.create(
            date=date,
            start_hour=start_hour,
            end_hour=end_hour,
            description=description,
            participants=participants
        )
        response['success'] = True
        response['message'] = 'Meeting created successfully'
        response['id'] = Meet.objects.latest('id').id
        return JsonResponse(response)
    
    def put(self, request):
        # This method will update an existing meeting in the database.
        meet_data = json.loads(request.body)
        meet_id = meet_data.get('id')
        date = meet_data.get('date')
        start_hour = meet_data.get('start_hour')
        end_hour = meet_data.get('end_hour')
        description = meet_data.get('description')
        participants = meet_data.get('participants')
        response = {'success': False}
    
        if meet_id is None:
            return JsonResponse({'status': 'error', 'message': 'Missing meeting id'})
        
        meet = Meet.objects.filter(id=meet_id).first()
        if meet is None:
            return JsonResponse({'status': 'error', 'message': 'Meeting not found'})
        
        meet.date = date if date is not None else meet.date
        meet.start_hour = start_hour if start_hour is not None else meet.start_hour
        meet.end_hour = end_hour if end_hour is not None else meet.end_hour
        meet.description = description if description is not None else meet.description
        meet.participants = participants if participants is not None else meet.participants

        meet.save()
        response['success'] = True
        response['message'] = 'Meeting updated successfully'
        return JsonResponse(response)
    
    def delete(self, request):
        # This method will change the deleted field of a meeting to True.
        meet_data = json.loads(request.body)
        meet_id = meet_data.get('id')
        response = {'success': False}
    
        if meet_id is None:
            return JsonResponse({'status': 'error', 'message': 'Missing meeting id'})
        
        meet = Meet.objects.filter(id=meet_id).first()
        if meet is None:
            return JsonResponse({'status': 'error', 'message': 'Meeting not found'})
        
        meet.is_deleted = True
        meet.save()

        response['success'] = True
        response['message'] = 'Meeting deleted successfully'
        return JsonResponse(response)
