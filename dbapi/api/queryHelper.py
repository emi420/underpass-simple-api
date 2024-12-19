def hashtags(hashtagsList):
    return "EXISTS ( SELECT * from unnest(hashtags) as h where {condition} )".format(
        condition=' OR '.join(
            map(lambda x: "h ~* '^{hashtag}'".format(hashtag=x), hashtagsList)
        )
    )

def bbox(wktMultipolygon):
    return "ST_Intersects(bbox, ST_GeomFromText('{area}', 4326))".format(
        area=wktMultipolygon
    )
