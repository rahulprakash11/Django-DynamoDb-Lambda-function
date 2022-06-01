from django.db import models as basemodels

from pynamodb import models
from pynamodb.attributes import UnicodeAttribute, JSONAttribute, ListAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection, IncludeProjection

from env import DB_HOST


class StageIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        index_name = 'productList'
        read_capacity_units = 5
        write_capacity_units = 5
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
    status = UnicodeAttribute(null=True, default='restricted')
    stageIndex = StageIndex()
    template = JSONAttribute()
