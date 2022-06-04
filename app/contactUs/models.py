#from django.db import models
from pynamodb import models
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection, IncludeProjection
from env import DB_HOST

"""
purpose : str {design/developer/casual}
userName : str
userEmail : str
details : text field
timestamp : str (auto-generated)
locality : str (auto)
state : state (auto)
country : str (auto)
"""

class CountryIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = 'byCountryIndex'
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()
    country = UnicodeAttribute(hash_key=True)
    timeStamp = UTCDateTimeAttribute(range_key=True)


class PurposeIndex(GlobalSecondaryIndex):
    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = 'byPurposeIndex'
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()
    purpose = UnicodeAttribute(hash_key=True)
    timeStamp = UTCDateTimeAttribute(range_key=True)

# Create your models here.
class ContactUs(models.Model):
    class Meta:
        table_name = "contactUs-table"
        host = DB_HOST
        region = "ap-south-1"
        read_capacity_units = 5
        write_capacity_units = 5

    userEmail = UnicodeAttribute(hash_key=True, null=False)
    timeStamp = UnicodeAttribute(range_key=True, null=False)
    userName = UnicodeAttribute(null=False)
    details = UnicodeAttribute()
    purpose = UnicodeAttribute(null=False)
    locality = UnicodeAttribute()
    state = UnicodeAttribute()
    country = UnicodeAttribute()
    byCountry = CountryIndex()
    byPurpose = PurposeIndex()
    id = UnicodeAttribute()