from importlib.metadata import metadata
from operator import le
from select import select
from commands import *
import psycopg2

def run_command(connection,command,action,params=None):
    cur = connection.cursor()
    res = []
    try:
        cur.execute(command, params)
        if action == "SELECT":
            if cur.rowcount > 0:
                row = cur.fetchone()
                while row is not None:
                    res.append(row) 
                    row = cur.fetchone()
        if action == "DELETE":
            res = int(cur.statusmessage.split(" ")[-1])
        cur.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return res
    
def create_shard_table(node_names,shard_count):
    node_count = len(node_names)
    start = -1
    step = shard_count//node_count
    shard_table = [None for i in range(shard_count)]
    for i in range(shard_count):
        if i%step == 0:
            start += 1
            if start == node_count:
                start = 0
        shard_table[i] = node_names[start]
    return shard_table
    
def hash_distribution_value(value, shard_count):
    total = 0
    for c in value:
        total += int(ord(c)) 
    hash = total % shard_count
    return hash

def distribute_shard_tables(coordinator,nodes,shard_table,table_name,schema):
    for i in range(len(shard_table)):
        node = nodes[shard_table[i]]
        shard_name = table_name + "_" + str(i)
        metadata = (shard_name, table_name, i, shard_table[i], node.info.host, node.info.port)
        run_command(node,create_table_command(shard_name,schema),"CREATE")
        run_command(coordinator,insert_command("shards_table", 6 ),"INSERT",metadata)

def check_distributed_table_exist(coordinator, table_name):
        command = """
            SELECT * FROM distribution_table
            WHERE table_name = '{}';
        """.format(table_name)
        res = run_command(coordinator,command,"SELECT")
        return len(res) > 0

def create_distributed_table(session,table_name,schema,distribution_column,shard_count=8):
    if not check_distributed_table_exist(session.coordinator,table_name):
        run_command(session.coordinator,insert_command("distribution_table", 3),"INSERT",(table_name,distribution_column,shard_count))
        node_names = [name for name in session.workers.keys()]
        shard_table = create_shard_table(node_names,shard_count)
        distribute_shard_tables(session.coordinator,session.workers,shard_table,table_name,schema)
    else:
        print("This table has already been distributed before")
    