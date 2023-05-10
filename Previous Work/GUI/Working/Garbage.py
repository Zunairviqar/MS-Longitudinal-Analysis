# importing os module
import os
#
# # Directory Names
# directory_1 = "TP1"
# directory_2 = "TP2"
#
# # Parent Directory path
# x = os.getcwdb()
# print(x)
# y = str(x).replace("b'", '')
# z = y.replace("'", '')
# parent_dir = z
#
# # Path
# path = os.path.join(parent_dir, directory_1)
# try:
#     os.mkdir(path)
# except OSError as error:
#     print(error)
#
# path = os.path.join(parent_dir, directory_2)
# try:
#     os.mkdir(path)
# except OSError as error:
#     print(error)
warning = False

path = '/Users/zunairviqar/Desktop/t2_flair_sag_p2_1mm_FS_ellip_pf78_10'
path2 = '/Users/zunairviqar/Desktop/VFP'
files = os.listdir(path)

for i in files:
    if '.dcm' in i:
        print("x")
    else:
        warning = True
print(warning)
