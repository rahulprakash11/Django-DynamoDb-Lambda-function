from datetime import datetime
import json

from api.settings import NANO_ID as _A

from nanoid import generate
from app.productionLine.models import ProductionLine
from pynamodb.expressions.operand import Path


class DynamodbProductionLine:
    if not ProductionLine.exists():
        ProductionLine.create_table(wait=True)
        print("created the productionLine-table")

    def create(self, data : dict):
        product = ProductionLine()
        category = data['category']
        print(data)
        id = f"{category}_{generate(_A, 13)}"
        print("adg")
        while self.checkIdExists(id=id):
            id = f"{category}_{generate(_A, 13)}"
        print("asgda")

        print(data.keys())
        
        try:
            product.from_json(json.dumps(data))
        except Exception as e:
            print("erroe :", e)

        print("product :", product.attribute_values)
        product.id = id
        product.save()
        print("ho gaya")
        return {"id" : id}

    def delete(self, id : str):
        entity = self.getById(id=id)
        entity.delete()

    def getById(self, id : str):
        entity = ProductionLine.get(hash_key=id)
        return entity

    def getPaginationByStageQuery(self, limit : int, lastKey : str, stage : str):
        #if stage ==null then use other indexes
        productList = ProductionLine.stageIndex.query(stage, filter_condition=None, limit=int(limit), last_evaluated_key=lastKey)#filter_condition= Products.status == 'unrestricted'
        return productList

    def getPaginationByQuery(self, limit : int, lastKey : str, query : str):
        #TODO
        # pass query as a filter_condition
        productList = ProductionLine.query(filter_condition=None, limit=int(limit), last_evaluated_key=lastKey)#filter_condition= Products.status == 'unrestricted'
        return productList

    def getPaginationByScan(self, limit : int, lastKey : dict):
        # print("dffaf")
        productList = ProductionLine.scan(filter_condition=None, limit=int(limit), last_evaluated_key=lastKey)#filter_condition= Products.status == 'unrestricted'
        # print("size",productList.__sizeof__())
        # print("jsadhadhas")
        return productList    

    def updateSelfAttributes(self, entity : ProductionLine, data : dict):
        actions = []
        for key in data.keys():
            if (key != "id"):
                value = data.get(key)
                actions.append(Path(key).set(value))
        entity.update(actions=actions)
        return entity

    def checkIdExists(self, id : str):
        try:
            return ProductionLine.get(hash_key=id).exists()
        except Exception as e:
            print(e)
            return False

