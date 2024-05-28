import os, time

path_check = ""
before_list = os.listdir(path_check)
print(before_list)

while True:
    # print("Start countdown")
    time.sleep(5)
    # print("Ent countdown")
    after_list = os.listdir(path_check)
    # print("After list ", after_list)
    added = [add for add in after_list if not add in before_list]
    removed = [remove for remove in before_list if not remove in after_list]
    before_list = after_list

    # print("add file" , added)
    # print("remove file" , removed)
    # print("before list" , before_list)