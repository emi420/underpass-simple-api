from dataclasses import dataclass
from .filters import tagsQueryFilter, hashtagQueryFilter
from enum import Enum
from .config import RESULTS_PER_PAGE, DEBUG
from .sharedTypes import Table, GeoType
from .serialization import deserializeTags
import json

# Build and run queries for getting geometry features
# (Points, LinesStrings, Polygons) from the Raw OSM Data DB

# Order by
class OrderBy(Enum):
    closedAt = "closed_at"
    id = "id"
    timestamp = "timestamp"

# DB table names
class Table(Enum):
    nodes = "nodes"
    lines = "ways_line"
    polygons = "ways_poly"
    relations = "relations"

# OSM types
class OsmType(Enum):
    nodes = "node"
    lines = "way"
    polygons = "way"

# Raw Features parameters  DTO
@dataclass
class RawFeaturesParamsDTO:
    area: str = None
    tags: list[str] = None
    hashtag: str = ""
    dateFrom: str = ""
    dateTo: str = ""
    table: Table = Table.nodes

# Build queries for getting geometry features
def geoFeaturesQuery(params: RawFeaturesParamsDTO, asJson: bool = False):
    geoType:GeoType = GeoType[params.table.name]
    query = "SELECT '{type}' as type, \
            osm_id as id, \n \
            timestamp, \n \
            ST_AsText(geom) as geometry, \n \
            tags, \n \
            hashtags, \n \
            editor, \n \
            closed_at \n \
            FROM {table} \n \
            LEFT JOIN changesets c ON c.id = {table}.changeset \n \
            WHERE{area}{tags}{hashtag}{date} {limit}; \n \
        ".format(
            type=geoType.value,
            table=params.table.value,
            area=" AND ST_Intersects(\"geom\", ST_GeomFromText('MULTIPOLYGON((({area})))', 4326) ) \n"
                .format(area=params.area) if params.area else "",
            tags=" AND (" + tagsQueryFilter(params.tags, params.table.value) + ") \n" if params.tags else "",
            hashtag=" AND " + hashtagQueryFilter(params.hashtag, params.table.value) if params.hashtag else "",
            date=" AND closed_at >= {dateFrom} AND closed_at <= {dateTo}\n"
                .format(dateFrom=params.dateFrom, dateTo=params.dateTo) 
                if params.dateFrom and params.dateTo else "\n",
            limit=" LIMIT {limit}".format(limit=RESULTS_PER_PAGE)
        ).replace("WHERE AND", "WHERE")

    if asJson:
        return rawQueryToJSON(query, params)

    return query

# Build queries for returning a raw features as a JSON (GeoJSON) response
def rawQueryToJSON(query: str, params: RawFeaturesParamsDTO):
    jsonQuery = "with predata AS \n ({query}) , \n \
        t_features AS ( \
            SELECT jsonb_build_object( 'type', 'Feature', 'id', id, 'properties', to_jsonb(predata) \
            - 'geometry' , 'geometry', ST_AsGeoJSON(geometry)::jsonb ) AS feature FROM predata  \
        ) SELECT jsonb_build_object( 'type', 'FeatureCollection', 'features', jsonb_agg(t_features.feature) ) \
        as result FROM t_features;" \
        .format(
            query=query.replace(";","")
        )
    if DEBUG:
        print(jsonQuery)
    return jsonQuery

# This class build and run queries for OSM Raw Data
class Raw:
    def __init__(self,db):
        self.db = db

    # Get geometry features (lines, nodes, polygons or all)
    async def getFeatures(
        self,
        params: RawFeaturesParamsDTO,
        featureType: GeoType = None,
        asJson: bool = False
    ):
        if featureType == "line":
            return self.getLines(params, asJson)
        elif featureType == "node":
            return self.getNodes(params, asJson)
        elif featureType == "polygon":
            return self.getPolygons(params, asJson)
        else:
            return await self.getAll(params, asJson)

    # Get polygon features
    async def getPolygons(
        self,
        params: RawFeaturesParamsDTO,
        asJson: bool = False
    ):
        params.table = Table.polygons
        result = await self.db.run(geoFeaturesQuery(params, asJson), asJson=asJson)
        if asJson:
            return result or {}
        return deserializeTags(result)

    # Get line features
    async def getLines(
        self,
        params: RawFeaturesParamsDTO,
       asJson: bool = False
    ):
        params.table = Table.lines
        result =  await self.db.run(geoFeaturesQuery(params, asJson), asJson=asJson)
        if asJson:
            return result or {}
        return deserializeTags(result)


    # Get node features
    async def getNodes(
        self,
        params: RawFeaturesParamsDTO,
        asJson: bool = False
    ):
        params.table = Table.nodes
        result = await self.db.run(geoFeaturesQuery(params, asJson), asJson=asJson)
        if asJson:
            return result or {}
        return deserializeTags(result)

    # Get all (polygon, line, node) features
    async def getAll(
        self,
        params: RawFeaturesParamsDTO,
        asJson: bool = False
    ):
        if asJson:

            polygons = json.loads(await self.getPolygons(params, asJson))
            lines = json.loads(await self.getLines(params, asJson))
            nodes = json.loads(await self.getNodes(params, asJson))

            jsonResult = {'type': 'FeatureCollection', 'features': []}

            if polygons and "features" in polygons and polygons['features']:
                jsonResult['features'] = jsonResult['features'] + polygons['features']

            if lines and "features" in lines and lines['features']:
                jsonResult['features'] = jsonResult['features'] + lines['features']

            elif nodes and "features" in nodes and nodes['features']:
                jsonResult['features'] = jsonResult['features'] + nodes['features']
        
            # elif relations and "features" in relations and relations['features']:
            #     result['features'] = result['features'] + relations['features']

            result = json.dumps(jsonResult)
            return result

        else:
            polygons = await self.getPolygons(params)
            lines = await self.getLines(params)
            nodes = await self.getNodes(params)
            result = [polygons, lines, nodes]
            return result

    