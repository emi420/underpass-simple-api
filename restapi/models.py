from pydantic import BaseModel

class Item(BaseModel):
    name: str

class BaseRequest(BaseModel):
    area: str = None
    tags: str = None
    hashtag: str = None
    dateFrom: str = None
    dateTo: str = None
    featureType: str = None
    osm_id: str = None
    order_by: str = None
    limit: str = "500"

class RawRequest(BaseRequest):
    pass
