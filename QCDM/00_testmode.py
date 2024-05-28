
import threading
import queue

my_queue = queue.Queue()

def storeInQueue(f):
  def wrapper(*args):
    my_queue.put(f(*args))
  return wrapper


@storeInQueue
def get_name(full_name):
   return full_name, full_name



t = threading.Thread(target=get_name, args = ("foo", ))
t.start()
t.join()

my_data = my_queue.get()
print(my_data)


# status == True
def QCstatus_check(status): return "PASS" if (status == True or status == "skip") else "NOT PASS" if status == False else status

print(QCstatus_check("Error"))
print(QCstatus_check(False))
print(QCstatus_check("skip"))

print("iii" and "po" and "po" and "Error" and True)


b = [True, False, False, True, "pa", "pa"]
bb = True
for i in b:
  bb = bb and i

print(bb)
print("=================================")
Lost_status = True
Angle_status = False
complete_status = "SKIP"
no_data_status = False
mode_status = False
validation_status = "SKIP"

QC_status_list = [Lost_status, Angle_status, complete_status, no_data_status, mode_status, validation_status]
QC = True
print("QC = ", QC_status_list)
for i in range(len(QC_status_list)):
  if QC_status_list[i] == "SKIP":
    QC_status_list[i] = True
  # elif QC_status_list[i] == "ERROR":
print("QC = ", QC_status_list)
for ii in QC_status_list:
  if ii == "ERROR":
    QC = "ERROR"
    break
  else:
    QC= QC and ii

print("QC = ", QC_status_list)
print("QC status : ", QC)