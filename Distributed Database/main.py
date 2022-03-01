from init import Session
from commands import *
from utils import *
from querry_planner import QuerryPlanner

sess = Session()
querry = QuerryPlanner()

schema = [["id", "text"],["name","text"]]
create_distributed_table(sess,"students",schema,0)

schema = [["course_name", "text"],["student_id","text"]]
create_distributed_table(sess,"course_enrollment",schema,1)

while True:
    prompt_string = """Choose an options below:
    1. View all student
    2. Create a new student
    3. Show course enrollment
    4. Enroll a student
    5. Delete a student by id
    6. Exit
    """

    print(prompt_string)
    option = ""
    try:
        option = int(input())
    except:
        print("Option must be a number")

    if option < 1 or option > 6:
        print("Invalid option")
    else:
        if option == 1:
            for s in querry.select_all(sess,"students"):
                print(s)
        if option == 2:
            student_id = input("Enter student id: ")
            student_name = input("Enter student name: ")
            try:
                querry.insert_single(sess,'students',(student_id,student_name))
            except:
                print("Some error happened, please try again: ")
        if option == 3:
            for c in querry.join(sess,'students','course_enrollment',('id','student_id'),("student_id","name","course_name")):
                print(c)
        if option == 4:
            student_id = input("Enter student id: ")
            course_name = input("Enter course name: ")
            try:
                querry.insert_single(sess, 'course_enrollment', (course_name, student_id))
            except:
                print("Some error happened, please try again: ")
        if option == 5:
            student_id = input("Enter student id: ")
            try:
                querry.delete_by_column(sess, 'students', 'id', student_id)
                querry.delete_by_column(sess, 'course_enrollment', 'student_id', student_id)
            except:
                print("Some error happened, please try again: ")
        if option == 6:
            print("Quitting")
            break