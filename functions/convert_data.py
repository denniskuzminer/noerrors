# import os
# import csv

# directory = "C:/Users/denni/Comp Sci/TECHUB24/NoErrors/functions/guardian_data"


# for filename in os.listdir(directory):
#     f = os.path.join(directory, filename)
#     if os.path.isfile(f):
#         with open(f) as file:
#             print(filename)
#             reader = csv.reader(file, delimiter=",", quotechar="|")
#             for row in reader:
#                 print(row)
#                 if row[0] !='':
