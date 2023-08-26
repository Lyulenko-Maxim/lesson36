import os
import psycopg2
from dotenv import load_dotenv


class PostgresDBMS:
    working = True


class AbstractManagerConnector:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        raise NotImplementedError


class PGManagerConnector(AbstractManagerConnector):
    def __init__(self, host, port, username, password, database):
        super().__init__(host = host, port = port)
        self.__username: str = username
        self.__password: str = password
        self.__database: str = database

    def connect(self):
        PostgresDBMS.working = True
        dsn = f"postgresql://{self.__username}:{self.__password}@{self.host}:{self.port}/{self.__database}"

        try:
            psycopg2.connect(dsn = dsn)

        except psycopg2.Error as err:
            PostgresDBMS.working = False
            print(err)

        finally:
            if PostgresDBMS.working:
                print(f"Connected to {self.host}:{self.port}")
            else:
                print("Connection refused")


load_dotenv()

pg_connector = PGManagerConnector(
    host = '127.0.0.1',
    port = '5432',
    username = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_NAME'),
)
pg_connector.connect()
