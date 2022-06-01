import json
from django.http import HttpRequest, QueryDict

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from app.products.dynamodb_interface import DynamodbProducts

# logger
import logging
logger = logging.getLogger(__name__)

logger.debug("this is a debug message!")
logger.info("this is an info message!!")
logger.error("this is an error message!!")


class ProductsView(APIView):
# POST
    def post(self, request, **kwargs):
        dynamodbProducts = DynamodbProducts()
        try:
            x : HttpRequest = request
            a = x.data
            if type(a) is dict:
                z = a
            elif type(a) is QueryDict:
                try:
                    y = a.dict()
                    z=y["_content"]
                    z=json.loads(z)
                except Exception as e:
                    print("err :", e)
            else:
                z = x.data

            keys = dynamodbProducts.create(data=z)
            context = {"isSuccessfull" : "true", "keys" : keys, "id":keys["id"]}
            return Response(status=status.HTTP_201_CREATED, data=context)
        except Exception as e:
            print("err :", e)
            return Response({'isSuccessful' : 'false'}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get(self, request, **kwargs):
        dynamodbProducts = DynamodbProducts()

        # getting category index value
        category : str = kwargs.get('category', 'app')

        filter = request.query_params.get('filter')
        if filter != None:
            filter = json.loads(filter)
            if "category" in filter.keys():
                category = filter["category"]

        if 'category' in request.query_params.keys():
            category : str = request.query_params.get('category')
        lastKey : str = request.query_params.get('lastKey')

        if lastKey:
            lastKey = lastKey.replace("\'", "\"")
            de = json.loads(lastKey)
            lastKey = de
        

        totalItemCount : int = request.query_params.get('totalItemCount', 0)
        limit : int = request.query_params.get('limit', 9)
        try:
            if category == 'all':
                productItter = dynamodbProducts.getPaginationByScan(limit=int(limit), lastKey=lastKey)
            else:
                productItter = dynamodbProducts.getPaginationByQuery(category=category, limit=int(limit), lastKey=lastKey)
            l = []
            for item in productItter:
                formatItem :dict = json.loads(item.to_json())
                l.append(formatItem)
            
            newLastKey = productItter.last_evaluated_key
            context = {'items' : l, "lastKey" : newLastKey, "totalItemCount" : totalItemCount + productItter.total_count, "limit" : int(limit)}
            contentRange =  "0-3/5"
            return Response(status=status.HTTP_200_OK, headers={"Content-Range" : contentRange}, data=context)

        except Exception as e:
            print("err :", e)
            return Response({'isSuccessful' : 'false'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# DELETE Many

    def delete(self, request, **kwargs):
        if "filter" in request.query_params.keys():
            filter : dict = json.loads(request.query_params.get("filter"))
        else:
            return Response({'isSuccessful': 'False', "message": "pass array of ids to delete in filter query params with key 'id"}, status= status.HTTP_400_BAD_REQUEST)

        ids : list[str] = filter.get("id", None)
        dynamodbProducts = DynamodbProducts()
        if ids != None:
            try:
                for id in ids:
                    _id = id.split("_")
                    dynamodbProducts.delete(category=_id[0], id=id)
                return Response(status=status.HTTP_200_OK, data=ids)
            except Exception as e:
                print("err :", e)
                return Response({'isSuccessful': 'False', "ids":ids}, status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'isSuccessful': 'False', "message": "pass array of ids to delete in filter query params with key 'id"}, status= status.HTTP_400_BAD_REQUEST)



class ProductDetailView(APIView):
# GET
    def get(self, request, id:str):
        category = id.split("_")[0]
        dynamodbProducts = DynamodbProducts()
        try:
            item = dynamodbProducts.getByPK(category=category, id=id)
            data = json.loads(item.to_json())
            context = {'item' : data}
            return Response(status=status.HTTP_200_OK, data=context)
        except Exception as e:
            print("err :", e)
            return Response({'isSuccessful' : 'false'}, status= status.HTTP_204_NO_CONTENT)

# PUT    
    def put(self, request, id:str):
        category = id.split("_")[0]

        dynamodbProducts = DynamodbProducts()
        try:
            entity = dynamodbProducts.getByPK(category=category, id=id)
            request.data.pop("id")
            request.data.pop("category")

            entity = dynamodbProducts.updateSelfAttributes(entity=entity, data=request.data)
            item = json.loads(entity.to_json()) 
            return Response({'isSuccessful' : 'true', "item":item}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print("err :", e)
            return Response({'isSuccessful' : 'false'}, status= status.HTTP_400_BAD_REQUEST)

# DELETE                        
    def delete(self, request, id:str):
        category = id.split("_")[0]

        dynamodbProducts = DynamodbProducts()
        try:
            dynamodbProducts.delete(category=category, id=id)
            return Response({'isSuccessful' : 'true'}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print("err :", e)
            return Response({'isSuccessful' : 'false'}, status= status.HTTP_400_BAD_REQUEST)

