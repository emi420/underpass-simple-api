from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import RawRequest
import raw
import config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Index:
    @app.get("/")
    async def index():
        return {"message": "This is an Underpass REST API."}

# Raw OSM Data

class Raw:
    @app.get("/raw/polygons")
    async def polygons(request: RawRequest):
        return await raw.polygons(request)

    @app.get("/raw/nodes")
    async def nodes(
        area: str = "",
        tags: str = "",
        hashtag: str= "",
        dateFrom: str = "",
        dateTo: str= ""
    ):
        request = RawRequest(
            area=area,
            tags=tags,
            hashtag=hashtag,
            dateFrom=dateFrom,
            dateTo=dateTo
        )
        return await raw.nodes(request)

    @app.get("/raw/lines")
    async def lines(
        area: str = "",
        tags: str = "",
        hashtag: str= "",
        dateFrom: str = "",
        dateTo: str= ""
    ):
        request = RawRequest(
            area=area,
            tags=tags,
            hashtag=hashtag,
            dateFrom=dateFrom,
            dateTo=dateTo
        )
        return await raw.lines(request)

    @app.get("/raw/features")
    async def features(
        area: str = "",
        tags: str = "",
        hashtag: str= "",
        dateFrom: str = "",
        dateTo: str= ""
    ):
        request = RawRequest(
            area=area,
            tags=tags,
            hashtag=hashtag,
            dateFrom=dateFrom,
            dateTo=dateTo
        )
        return await raw.features(request)

