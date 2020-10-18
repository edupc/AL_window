from datetime import datetime,timezone,timedelta
import os
# dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
# dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
#
# print(dt2.strftime("%Y-%m-%d'%Hh%Mm%Ss'")) # 將時間轉換為 string
#
# product_name = ('AL%s%s' % (str(100.0), str(500.0)))
# dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
# dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區
#         #print(dt2.strftime("%Y-%m-%d'%Hh%Mm%Ss'"))  # 將時間轉換為 string
# print(dt2.strftime)
# file_name = ("%s-%s" % (product_name, dt2.strftime("%Y-%m-%d'%Hh%Mm%Ss'")))
# save_dir ='C:\\Users\\PDAL-BM-1\\Desktop'
# try:
#     save_dir = '\\'.join(save_dir.split('/'))  # if using GUI to set file_dir
# except:  # if using API call method, which file_dir has benn processed
#     pass
# newpath = os.path.join(save_dir, file_name)
# print(newpath)
# if not os.path.exists(newpath):
#     os.makedirs(newpath)
# print(newpath)
def save_dir(save_dir):
    time_now = datetime.now()
    # 資料夾名稱
    product_name = ('AL%s%s' % (str(int(500)), str(int(500))))
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區
    # print(dt2.strftime("%Y-%m-%d'%Hh%Mm%Ss'"))  # 將時間轉換為 string
    print(dt2.strftime("%Y-%m-%d'%Hh%Mm%Ss'"))
    file_name = ("%s-%s" % (product_name, dt2.strftime("%Y-%m-%d'%Hh%Mm%Ss'")))

    try:
        save_dir = '\\'.join(save_dir.split('/'))  # if using GUI to set file_dir
    except:  # if using API call method, which file_dir has benn processed
        pass
    newpath = os.path.join(save_dir, file_name)
    print(newpath)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
save_dir('C:\\Users\\PDAL-BM-1\\Desktop')