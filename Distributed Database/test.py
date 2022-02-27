from calendar import c
from init import Session
from commands import *
from utils import *
from querry_planner import QuerryPlanner
sess = Session()

schema = [["id", "text"],["name","text"]]
create_distributed_table(sess,"students",schema,0)
querry = QuerryPlanner()
querry.insert_single(sess, "students", ("BI10-154","Nguyen Tuong Quynh"))
querry.insert_single(sess, "students", ("BI10-098","Mai Xuan Hieu"))
querry.insert_single(sess, "students", ("BI10-146","Nguyen Anh Quan"))
querry.insert_single(sess, "students", ("BI10-195","Nguyen Quang Vinh"))
querry.insert_single(sess, "students", ("BI10-128","Nguyen Tran Nguyen"))

print(querry.select_all(sess,"students"))
# querry.delete_by_column(sess,"students","name", "Nguyen Tran Nguyen")