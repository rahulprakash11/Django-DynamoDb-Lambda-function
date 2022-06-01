import json

from nanoid import generate
from django_dynamodb_lambda_function.settings import NANO_ID as _A
from app.products.models import Products
from pynamodb.expressions.operand import Path


class DynamodbProducts:
    def __init__(self) -> None:
        if not Products.exists():
            Products.create_table(wait=True)
            print("created the products-table")

    def create(self, data : dict, keepID : bool=False):
        product = Products()
        category = data['category']
        if 'id' in data.keys() and keepID:
            id = data['id']
        else:
            _id = generate(_A, 13)
            id = f"{category}_{_id}"
        while self.checkPkExists(category=category, id=id):
            id = f"{category}_{generate(_A, 13)}"
        

        product.from_json(json.dumps(data))
        product.id = id
        product.save()
        keys = {"category" : category, "id" : id}
        return keys

    def delete(self, category : str, id : str):
        entity = self.getByPK(category=category, id=id)
        entity.delete()

    def getByPK(self, category: str, id : str):
        entity = Products.get(hash_key=category, range_key=id)
        return entity

    def getById(self, id:str):
        x = id.split("_")
        category = x[0]
        entity = Products.get(hash_key=category, range_key=id)
        return entity

    def getPaginationByQuery(self, limit : int, lastKey : str, category : str):
        productItter = Products.query(hash_key=category, filter_condition=None, limit=int(limit), last_evaluated_key=lastKey)#filter_condition= Products.status == 'unrestricted'
        return productItter

    def getPaginationByScan(self, limit : int, lastKey : dict):
        productList = Products.scan(filter_condition=None, limit=int(limit), last_evaluated_key=lastKey)#filter_condition= Products.status == 'unrestricted'
        return productList

    def updateSelfAttributes(self, entity : Products, data : dict):
        actions = []
        keys = entity.attribute_values.keys()
        for key in data.keys():
            if (key != "id") or (key != "category"):
                value = data.get(key)
                actions.append(Path(key).set(value))
        entity.update(actions=actions)
        return entity

    def checkPkExists(self, category : str, id : str):
        try:
            return Products.get(hash_key=category, range_key=id).exists()
        except Exception as e:
            return False
