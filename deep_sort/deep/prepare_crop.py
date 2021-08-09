import os
from shutil import copyfile
# from distutils.dir_util import copy_tree

# You only need to change this line to your dataset download path
download_path = 'crops'

if not os.path.isdir(download_path):
    print('please change the download_path')

save_path = download_path + '/pytorch'
if not os.path.isdir(save_path):
    os.mkdir(save_path)
 
#-----------------------------------------
#query and gallery
print("====Generate query/gallery direcotry====")
query_path = download_path + '/test'
query_save_path = download_path + '/pytorch/query'
gallery_save_path = download_path + '/pytorch/gallery'
if not os.path.isdir(query_save_path):
    os.mkdir(query_save_path)
if not os.path.isdir(gallery_save_path):
    os.mkdir(gallery_save_path)

for _, dirs, _ in os.walk(query_path, topdown=True):
    for i in dirs:
        for _, _, files in os.walk(os.path.join(query_path, i), topdown=True):
            check = int(len(files)/6)
            if check <= 1:
                check = 1
            if(len(files) <= 1):
                print('{}, files_no:{} (ByPass)'.format(i, len(files)))
                continue
            print('{}, files_no:{}, query_no:{}, gallery_no:{}'.format(i, len(files), check, len(files)-check))
            for j, f in enumerate(files):
                if not os.path.isdir(os.path.join(query_save_path, i)):
                    os.mkdir(os.path.join(query_save_path, i))
                if not os.path.isdir(os.path.join(gallery_save_path, i)):
                    os.mkdir(os.path.join(gallery_save_path, i))
                src_path = os.path.join(query_path, i)
                dst_path = None
                if(j<=check):
                    dst_path = os.path.join(query_save_path, i)
                else:
                    dst_path = os.path.join(gallery_save_path, i)
                if not os.path.isdir(dst_path):
                    os.mkdir(dst_path)
                copyfile(os.path.join(src_path, f), os.path.join(dst_path, f))

            
#---------------------------------------
#train
print("\n====Generate train direcotry====")
train_path = download_path + '/train'
train_save_path = download_path + '/pytorch/train'
if not os.path.isdir(train_save_path):
    os.mkdir(train_save_path)

# copy_tree(train_path, train_save_path)
for _, dirs, _ in os.walk(train_path, topdown=True):
    for i in dirs:
        for _, _, files in os.walk(os.path.join(train_path, i), topdown=True):
            print('{}, files_no:{}'.format(i, len(files)))
            for j, f in enumerate(files):
                src_path = os.path.join(train_path, i)
                dst_path = os.path.join(train_save_path, i)
                if not os.path.isdir(dst_path):
                    os.mkdir(dst_path)
                copyfile(os.path.join(src_path, f), os.path.join(dst_path, f))
