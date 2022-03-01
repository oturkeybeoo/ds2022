def create_table_command(table_name,schema):
    command = "CREATE TABLE {} (".format(table_name)    
    for field in schema:
        command += "{} {},".format(field[0], field[1])

    command = command[:-1] + ");"

    return command

def insert_command(table_name, value_count):
    value_field = ",".join(["%s" for i in range(value_count)])
    command = "INSERT INTO {} VALUES({});".format(table_name, value_field)
    return command

def select_all_command(table_name):
    command = "SELECT * FROM {};".format(table_name)
    return command

def delete_by_column_command(table_name, column, value):
    command = """
        DELETE FROM {} WHERE {} = '{}';
    """.format(table_name,column,value)
    return command

def join_command(table_1, table_2, join_columns, select_columns):
    columns_string = ", ".join([c for c in select_columns])
    command = """
        SELECT {} from {} JOIN {}
        ON {}.{} = {}.{};
    """.format(columns_string, table_1,table_2,table_1,join_columns[0],table_2,join_columns[1])
    return command