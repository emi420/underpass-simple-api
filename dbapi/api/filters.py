def tagsQueryFilter(tagsQuery, table):
    query = ""
    tags = tagsQuery.split(",")
    keyValue = tags[0].split("=")

    if len(keyValue) == 2:
        query += "{table}.tags->>'{key}' ~* '^{value}'".format(
            table=table,
            key=keyValue[0],
            value=keyValue[1]
        )
    else:
        query += "{table}.tags->>'{key}' IS NOT NULL".format(
            table=table, 
            key=keyValue[0]
        )

    for tag in tags[1:]:
        keyValue = tag.split("=")
        if len(keyValue) == 2:
            query += "OR {table}.tags->>'{key}' ~* '^{value}'".format(
                table=table,
                key=keyValue[0],
                value=keyValue[1]
            )
        else:
            query += "OR {table}.tags->>'{key}' IS NOT NULL".format(
                table=table,
                key=keyValue[0]
            )
    return query

def hashtagQueryFilter(hashtag, table):
    return "'{hashtag}' = ANY (hashtags)".format(
        hashtag=hashtag
    )
