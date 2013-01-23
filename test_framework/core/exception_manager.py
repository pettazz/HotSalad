import uuid
from test_framework.core.mysql import DatabaseManager

class ExceptionManager:
    """
    Helper for exception tracking in the DB
    """

    def __init__(self, database_env):
        self.database_env = database_env

    def get_guid_for_hash(self, hash):
        params = {"hash": hash}
        query = """SELECT guid FROM exception
                   WHERE hash = %(hash)s"""
        guid = DatabaseManager(self.database_env).fetchone_query_and_close(query, params)
        if guid is None:
            guid = str(uuid.uuid4())
            params['guid'] = guid
            query = """INSERT INTO exception (guid, hash)
                       VALUES (%(guid)s, %(hash)s)"""
            DatabaseManager(self.database_env).execute_query_and_close(query, params)
        else:
            guid = guid[0]

        return guid