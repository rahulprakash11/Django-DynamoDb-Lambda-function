import datetime
from dateutil import parser
import json
from app.contactUs.models import ContactUs
from pynamodb.expressions.operand import Path



class DynamodbContactUs:
    if not ContactUs.exists():
        ContactUs.create_table(wait=True)
        print("created the contactUs-table")

    def create(self, data : dict):
        contact = ContactUs()
        contact.from_json(json.dumps(data))
        # timeNow = datetime.datetime.now()
        contact.timeStamp = f"{datetime.datetime.now()}"
        id = f"{contact.userEmail}+{contact.timeStamp}"
        contact.id = id
        contact.save()
        keys = {"id" : id}
        # print("contactss :", ContactUs.get)
        return keys
    pass

    def getPaginationByScan(self, limit : int, lastKey):
        try:
            contactList = ContactUs.scan(filter_condition=None, limit=int(limit), last_evaluated_key=lastKey)
            return contactList
        except Exception as e:
            print("err :", e )
            contactList = ContactUs.scan(filter_condition=None, limit=int(limit))
            return contactList
        

    def getById(self, id:str):
        x = id.split("+")
        userEmail = x[0]
        timeStamp = x[1]
        # print(timestamp)
        # timeStamp = parser.parse(timestamp)
        # print(timeStamp)
        entity = ContactUs.get(hash_key=userEmail, range_key=timeStamp)
        return entity

    def getByPK(self, userEmail:str, timeStamp:str or datetime):
        if type(timeStamp) == str:
            timeStamp = parser.parse(timeStamp)
        entity = ContactUs.get(hash_key=userEmail, range_key=timeStamp)
        return entity

    def delete(self, id:str):
        entity = self.getById(id=id)
        entity.delete()


    def updateSelfAttributes(self, entity : ContactUs, data : dict):
        actions = []
        keys = entity.attribute_values.keys()
        #check = True
        for key in keys:
            #check = check and key in keys
            if (key in data.keys()) and (key != "id" or "userEmail" or "timeStamp"):
                value = data.get(key)
                actions.append(Path(key).set(value))
        entity.update(actions=actions)
