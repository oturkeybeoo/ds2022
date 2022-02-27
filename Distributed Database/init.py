import psycopg2
import node_config
from utils import run_command
from commands import create_table_command

class Session():
    def __init__(self):
        self.coordinator, self.workers = self.load_nodes()
        if not self.check_table_exist("shards_table"):
            self.create_metadata_shards_table()
        if not self.check_table_exist("distribution_table"):
            self.create_metadata_distribution_table()

    def check_table_exist(self,table_name):
        print("Checking {} existance.".format(table_name))
        command = """
            SELECT * FROM pg_catalog.pg_tables
            WHERE tablename = '{}';
        """.format(table_name)
        res = run_command(self.coordinator,command,"SELECT")
        if len(res) > 0:
            print("{} existed.".format(table_name))
            return True
        else:
            print("{} does not exist.".format(table_name))
            return False

    def create_metadata_shards_table(self):
        print("Initializing shards table.")
        schema = (("shard_name", "text"),
                  ("table_name", "text"),
                  ("table_index","int"),
                  ("node_name","text"),
                  ("host", "text"),
                  ("port", "int"))

        run_command(self.coordinator,create_table_command("shards_table", schema),"CREATE")
        print("Shard table initialized")
    
    def create_metadata_distribution_table(self):
        print("Initializing distribution table.")
        schema = (("table_name", "text"),
                  ("distribution_column", "int"),
                  ("shard_count", "int"))

        run_command(self.coordinator,create_table_command("distribution_table", schema),"CREATE")
        print("Distribution table initialized")

    def load_nodes(self):
        print("Connecting to coordinator node.")
        coordinator = self.connect_to_node(node_config.coordinator)
        print("Connection established")
        workers = {}
        for worker in node_config.workers:
            print("Connecting to worker:",worker[0])
            workers[worker[0]] = self.connect_to_node(worker[1])
            print("Connection established")
        return coordinator, workers

    def connect_to_node(self,dsn):
        conn = psycopg2.connect(dsn)
        return conn