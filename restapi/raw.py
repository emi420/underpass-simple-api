import sys,os
sys.path.append(os.path.realpath('../dbapi'))

from models import RawRequest
from api import raw as RawApi
from api.db import DB
import config
import json

db = DB(config.UNDERPASS_DB)
raw = RawApi.Raw(db)

async def polygons(request: RawRequest):
    return json.loads(await raw.getPolygons(
        RawApi.RawFeaturesParamsDTO(
            area = request.area,
            tags = request.tags,
            hashtag = request.hashtag,
            dateFrom = request.dateFrom,
            dateTo = request.dateTo,
            order_by = request.order_by,
            limit = request.limit,
        ), asJson=True)
    )

async def nodes(request: RawRequest):
    return json.loads(await raw.getNodes(
        RawApi.RawFeaturesParamsDTO(
            area = request.area,
            tags = request.tags,
            hashtag = request.hashtag,
            dateFrom = request.dateFrom,
            dateTo = request.dateTo,
            order_by = request.order_by,
            limit = request.limit,
        ), asJson=True)
    )

async def lines(request: RawRequest):
    return json.loads(await raw.getLines(
        RawApi.RawFeaturesParamsDTO(
            area = request.area,
            tags = request.tags,
            hashtag = request.hashtag,
            dateFrom = request.dateFrom,
            dateTo = request.dateTo,
            order_by = request.order_by,
            limit = request.limit,
        ), asJson=True)
    )

async def features(request: RawRequest):
    return json.loads(await raw.getFeatures(
        RawApi.RawFeaturesParamsDTO(
            area = request.area,
            tags = request.tags,
            hashtag = request.hashtag,
            dateFrom = request.dateFrom,
            dateTo = request.dateTo,
            osm_id = request.osm_id,
            order_by = request.order_by,
            limit = request.limit,
       ), asJson=True)
    )

