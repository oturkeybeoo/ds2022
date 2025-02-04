from ntpath import join
from utils import *

class QuerryPlanner():
    def get_node_by_id(self,coordinator,id,table_name):
        sql = """
                SELECT node_name, shard_name FROM shards_table
                WHERE table_index = '{}' and table_name = '{}';
            """.format(id,table_name)
        res = run_command(coordinator,sql,"SELECT")
        return res 

    def insert_single(self,session,table_name,value):
        sql = """
                SELECT distribution_column, shard_count FROM distribution_table
                WHERE table_name = '{}';
            """.format(table_name)
        res = run_command(session.coordinator,sql,"SELECT")
        if len(res) > 0:
            distribution_column,shard_count = res[0]
            shard_id = hash_distribution_value(value[distribution_column],shard_count)

            node_name,shard_name = self.get_node_by_id(session.coordinator, shard_id,table_name)[0]
            run_command(session.workers[node_name],insert_command(shard_name,len(value)),"INSERT",value)
            print("Inserted into node {}, shard {}".format(node_name,shard_name))
        else:
            print("Relation does not exist")
            
    def select_all(self,session,table_name):
        res = []
        sql = """
                SELECT node_name, shard_name FROM shards_table
                WHERE table_name = '{}';
            """.format(table_name)
        shards = run_command(session.coordinator,sql,"SELECT")
        for shard in shards:
            res += run_command(session.workers[shard[0]],select_all_command(shard[1]),"SELECT")
            
        return res

    def join(self,session,table_1,table_2,join_columns,select_columns):
        res = []
        sql = """
                SELECT node_name, shard_name, table_index FROM shards_table
                WHERE table_name = '{}';
            """.format(table_1)
        shards = run_command(session.coordinator,sql,"SELECT")

        for shard in shards:
            command = join_command(shard[1], table_2+"_"+str(shard[2]), join_columns, select_columns)
            res += run_command(session.workers[shard[0]],command,"SELECT")
            
        return res

    def delete_by_column(self,session,table_name,column,value):
        sql = """
                SELECT node_name, shard_name FROM shards_table
                WHERE table_name = '{}';
            """.format(table_name)
        shards = run_command(session.coordinator,sql,"SELECT")
        for shard in shards:
            res = run_command(session.workers[shard[0]],delete_by_column_command(shard[1],column,value),"DELETE")
            if res > 0:
                print("Deleted {} record(s) in table {} at node {}".format(res,shard[1],shard[0]))