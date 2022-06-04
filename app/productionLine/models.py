from django.db import models as basemodels

# Create your models here.
from pynamodb import models
from pynamodb.attributes import UnicodeAttribute, JSONAttribute, ListAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection, IncludeProjection

from env import DB_HOST

'''
id : unique identifier
stage : proposed/ongoing/completed
name : "product's name"
detail : ["app, illustation, design,...", "blogging", "dummy app"]
attr : {platform:[android, web, ], type:{clone }, language:[kotlin, python, ]}
notes : ["Material design", "QR Scanner", "Jetpack"]
'''

class StageIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = 'productList'
        read_capacity_units = 5
        write_capacity_units = 5
        # not All attributes are projected
        projection = AllProjection()
    stage = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)


class ProductionLine(models.Model):
    
    class Meta:
        table_name = "productionLine-table"
        host = DB_HOST
        region = "ap-south-1"
        read_capacity_units=5
        write_capacity_units=5
    
    id = UnicodeAttribute(hash_key=True, range_key=True, null=False)
    stage = UnicodeAttribute(null=False)
    name = UnicodeAttribute(null=False)
    category = UnicodeAttribute(null=False)
    detail = UnicodeAttribute(null=True)
    notes = ListAttribute(null=True)
    attributes = ListAttribute(null=True)
    expiryDate = UnicodeAttribute(null=True)
    startDate = UnicodeAttribute(null=True)
    completionDate = UnicodeAttribute(null=True)
    voteCount = NumberAttribute(default=0)
    priorityCount = NumberAttribute(default=0)
    wtdPriority = NumberAttribute(default=0)
    progress = NumberAttribute(default=0)
    # sponsor = UnicodeSetAttribute() # need change
    status = UnicodeAttribute(null=True, default='restricted')
    stageIndex = StageIndex()
    template = JSONAttribute()
