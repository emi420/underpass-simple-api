import asyncpg
import json
from .config import DEBUG

class DB():
    # Default DB configuration
    
    def __init__(self, connectionString = None):
        self.connectionString = connectionString or "postgresql://underpass:underpass@localhost:5432/underpass"
        self.pool = None
        # Extract the name of the database
        self.name = self.connectionString[self.connectionString.rfind('/') + 1:]

    async def __enter__(self):
        await self.connect()

    async def connect(self):
        """ Connect to the database """
        print("Connecting to DB ... " + self.connectionString if DEBUG else "")
        if not self.pool:
            try:
                self.pool = await asyncpg.create_pool(
                    min_size=1,
                    max_size=10,
                    command_timeout=60,
                    dsn=self.connectionString,
                )
            except Exception as e:
                print("Can't connect!")
                print(e)

    def close(self):
        if self.pool is not None:
            self.pool.close()

    async def run(self, query, singleObject = False, asJson=False):
        if DEBUG:
            print("Running query ...")
        if not self.pool:
            await self.connect()
        if self.pool:
            result = None
            try:
                conn = await self.pool.acquire()
                result = await conn.fetch(query)
                data = None
                if asJson:
                    data = result[0]['result']
                elif singleObject:
                    data = result[0]
                else:
                    data = result
                await self.pool.release(conn)
                return data
            except Exception as e: 
                print("\n******* \n" + query + "\n******* \n")
                print(e)
                return None

