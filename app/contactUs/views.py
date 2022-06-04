import requests
import json

#from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.http import HttpRequest
from app.contactUs.dynamodb_interface import DynamodbContactUs



class ContactsView(APIView):
    def post(self, request):
        dynamodbContactUs = DynamodbContactUs()
        try:
            x : HttpRequest = request
            data = request.data
            ip = x.get_host()
            res = requests.get(f'https://ip-api.io/api/json?api_key={ip}')
            location_data = json.loads(res.text)
            data["locality"] = location_data['city']
            data["state"] = location_data['region_name']
            data["country"] = location_data['country_name']
            keys = dynamodbContactUs.create(data=data)
            return Response({"isSuccessful" : "true", "id" : keys["id"]}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("err :", e)
            return Response({'error': 'Failed to insert'}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        dynamodbContactUs = DynamodbContactUs()
        lastKey = request.query_params.get('lastKey')
        totalItemCount = request.query_params.get('totalItemCount', 0)
        limit = request.query_params.get('limit', 20)

        contacts = dynamodbContactUs.getPaginationByScan(limit=limit, lastKey=lastKey)
        l = []
        for item in contacts:
            l.append(json.loads(item.to_json()))
        context = {'items' : l, "lastKey" : contacts.last_evaluated_key, "totalItemCount" : totalItemCount + contacts.total_count, "pageSize" : 3}
        return Response(status=status.HTTP_200_OK, data=context)

    # def get(self, request):
    #     data = { "userEmail" : "email@email.com", "userName" : "compulsory", "details" : "text_field", "purpose" : "choice_field"}
    #     context = {"message" : "Contact Us!!!", "data" : data}
    #     return Response(data=context)



class ContactDetailView(APIView):
    def get(self, request : HttpRequest, id : str):
        dynamodbContactUs = DynamodbContactUs()
        try:
            item = dynamodbContactUs.getById(id=id)
            data = json.loads(item.to_json())
            return Response(status=status.HTTP_200_OK, data={"item":data})
        except Exception as e:
            print("err :", e)
            return Response({'error': "item doesn't exist"}, status= status.HTTP_404_NOT_FOUND)

    def put(self, request:HttpRequest, id:str):
        dynamodbContactUs = DynamodbContactUs()
        try:
            item = dynamodbContactUs.getById(id=id)
            dynamodbContactUs.updateSelfAttributes(entity=item, data=request.data)
            return Response({'isSuccessful' : 'true'}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print("err :", e)
            return Response({'error': 'Failed to update'}, status= status.HTTP_400_BAD_REQUEST)


    def delete(self, request:HttpRequest, id : str):
        dynamodbContactUs = DynamodbContactUs()
        try:
            dynamodbContactUs.delete(id=id)
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print("err :", e)
            return Response({'error': 'Failed to delete'}, status= status.HTTP_400_BAD_REQUEST)
        
