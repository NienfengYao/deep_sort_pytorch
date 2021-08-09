import os
from shutil import copyfile, move
import random

# You only need to change this line to your dataset download path
download_path = 'reid_dataset'
min_no = 50
percent_train_test = 0.7 # train:70%, test:30%

if not os.path.isdir(download_path):
    print('please change the download_path')

save_path = download_path + '/pytorch'
if not os.path.isdir(save_path):
    os.mkdir(save_path)

#-----------------------------------------
# Filter out pics < min_no
id_dict = {}
for root, dirs, files in os.walk(download_path, topdown=True):
    for name in files:
        if not name[-3:]=='jpg':
            continue
        ID  = name.split('_')[0]
        if len(id_dict) ==  0 or ID not in id_dict.keys():
            id_dict[ID] = [1, [name]]
        else:
            id_dict[ID][0] += 1
            id_dict[ID][1].append(name)
    break # only 1 level, avoid into sub dir
print('Original: id_no:{}, pic_no:{}'.format(len(id_dict.keys()), sum(v[0] for v in id_dict.values())))
id_dict = dict((k, v) for k, v in id_dict.items() if v[0] >= min_no)
print('After filter(pic_no>{}): id_no:{}, pic_no:{}'.format(min_no, len(id_dict.keys()), sum(v[0] for v in id_dict.values())))

#-----------------------------------------
#bounding_box_train/bounding_box_test
bounding_box_train_path= download_path + '/bounding_box_train'
bounding_box_test_path = download_path + '/bounding_box_test'
if not os.path.isdir(bounding_box_train_path):
    os.mkdir(bounding_box_train_path)
if not os.path.isdir(bounding_box_test_path):
    os.mkdir(bounding_box_test_path)

bounding_box_train_cnt = bounding_box_test_cnt = 0
for k, v in id_dict.items():
    random.shuffle(v[1])
    check = int(v[0]*percent_train_test)
    train_names = v[1][:check]
    test_names = v[1][check:]
    bounding_box_train_cnt += check
    bounding_box_test_cnt += (v[0] - check)
    for i in train_names:
        move(os.path.join(download_path, i), os.path.join(bounding_box_train_path, i))
    for i in test_names:
        move(os.path.join(download_path, i), os.path.join(bounding_box_test_path, i))
print('bounding_box_train:{}, bounding_box_test:{}'.format(bounding_box_train_cnt, bounding_box_test_cnt))

#-----------------------------------------
#test
test_path = download_path + '/bounding_box_test'
test_save_path = download_path + '/pytorch/test'
if not os.path.isdir(test_save_path):
    os.mkdir(test_save_path)

for root, dirs, files in os.walk(test_path, topdown=True):
    for name in files:
        if not name[-3:]=='jpg':
            continue
        ID  = name.split('_')
        src_path = test_path + '/' + name
        dst_path = test_save_path + '/' + ID[0]
        if not os.path.isdir(dst_path):
            os.mkdir(dst_path)
        copyfile(src_path, dst_path + '/' + name)

#-----------------------------------------
#query and gallery
print("====Generate query/gallery direcotry====")
query_path = download_path + '/pytorch/test'
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
#train_all
train_path = download_path + '/bounding_box_train'
train_save_path = download_path + '/pytorch/train'
if not os.path.isdir(train_save_path):
    os.mkdir(train_save_path)

for root, dirs, files in os.walk(train_path, topdown=True):
    for name in files:
        if not name[-3:]=='jpg':
            continue
        ID  = name.split('_')
        src_path = train_path + '/' + name
        dst_path = train_save_path + '/' + ID[0]
        if not os.path.isdir(dst_path):
            os.mkdir(dst_path)
        copyfile(src_path, dst_path + '/' + name)


