import win32com.client as win32
import datetime,string,os
import globals_var as gvar


#Part 開啟
def part_open(target,dir):
    catapp = win32.Dispatch("CATIA.Application")
    document = catapp.Documents
    # try:
    partdoc = document.Open("%s\%s.%s" % (dir,target,"CATPart"))
    # except:
    #     partdoc = document.Open("%s\%s.%s" % (dir,target,"CATProduct"))

#開啟零件檔案
def file_open(target,dir):
    #連結CATIA
    catapp = win32.Dispatch("CATIA.Application")
    document = catapp.Documents
    #將路徑設為目錄的文字宣告
    directory = str(dir)
    #directory = '\\'.join(directory.split('/'))
    print(directory)
    #gvar.folderdir = directory
    #定義零件檔檔名
    part_dir = directory+target+'.CATPart'
    print(part_dir)
    #partdoc = document.Open("%s%s.%s" % (directory,target,"CATPart"))
    #開啟該零件檔
    partdoc = document.Open(part_dir)
    return target+'.CATPart'
#開啟組立檔案
def assembly_open_file(folder,target,type):
    catapp = win32.Dispatch("CATIA.Application")
    productdoc = catapp.ActiveDocument
    product = productdoc.Product
    products = product.Products
    #print(type(gvar.folderdir))
    #print(type(target))
    #directory = '\\'.join(folder.split('/'))
    #開啟 0為零件檔/1為組立檔 進入該組立檔
    if type ==0:
        filedir = "%s\%s.%s" % (folder,target,"CATPart")
    elif type == 1:
        filedir = "%s\%s.%s" % (folder,target,"CATProduct")
    print(filedir)
    import_file = filedir,
    list(import_file)
    productsvarient = products.AddComponentsFromFiles(import_file,"All")
    return productsvarient

#改變parameter內的數值
def Sideplate_param_change(target,value):
    catapp = win32.Dispatch("CATIA.Application")
    partdoc = catapp.ActiveDocument
    part = partdoc.Part
    parameter = part.Parameters
    #按照介面輸入的參數找出相對應的面建出板子
    length = parameter.Item(target)
    if target == "width":
        length.Value = value
    elif target == "depth":
        D_value = float(value) + 14.5
        length.Value = D_value
    elif target == "height":
        length.Value = value
    part.Update()

def open_assembly():
    catapp = win32.Dispatch("CATIA.Application")
    document = catapp.Documents
    productdoc = document.Add("Product")
    product = productdoc.Product
    products = product.Products


def save_dir(save_dir):
    time_now = datetime.datetime.now()

    product_name=('AL%s%s'%(str(gvar.width), str(gvar.height)))
    year=str((int(time_now.strftime('%Y'))%1000)%100)
    code_E=list(string.ascii_uppercase)
    month=code_E[int(time_now.strftime('%m'))-1]
    code_e=list(string.ascii_lowercase)
    day =time_now.strftime('%d')
    hour=code_e[int(time_now.strftime('%H'))]
    minute=time_now.strftime('%M')

    file_name=('%s-%s%s%s%s%s'%(product_name,year,month,day,hour,minute))
    try:
        save_dir = '\\'.join(save_dir.split('/'))   # if using GUI to set file_dir
    except:     # if using API call method, which file_dir has benn processed
        pass
    newpath = os.path.join(save_dir, file_name)
    print(newpath)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

def saveas_close(save_dir,target,data_type):
    catapp = win32.Dispatch('CATIA.Application')
    document = catapp.Documents
    # catia 儲存只有組立跟零件，只有兩種可能並結果可預測
    try:
        saveas = document.Item('%s%s' % (target,data_type))
        saveas.SaveAs('%s\%s%s' % (save_dir,target,data_type))
    except:
        saveas = catapp.ActiveDocument
        saveas.SaveAs('%s\%s%s' % (save_dir,target,data_type))
    finally:
        saveas.Save()
       # saveas.Close()

def saveas_specify_target(save_dir,target,data_type):
    catapp = win32.Dispatch('CATIA.Application')
    doc = catapp.Documents
    saveas = doc.Item('%s.%s' % (target, data_type))
    saveas.Save()
    saveas.Close()

def saveas(save_dir, target, data_type):
    catapp = win32.Dispatch('CATIA.Application')
    document = catapp.Documents
    try:
        saveas = document.Item('%s%s' % (target, data_type))
        saveas.SaveAs('%s\%s%s' % (save_dir, target, data_type))
    except:
        saveas = catapp.ActiveDocument
        saveas.SaveAs('%s\%s%s' % (save_dir, target, data_type))
    finally:
        saveas.Save()

#增加偏移拘束
def add_offset_assembly(element1,element2,dist,relation):
    catapp = win32.Dispatch("CATIA.Application")
    productdoc = catapp.ActiveDocument
    product = productdoc.Product
    product = product.ReferenceProduct
    constraints = product.Connections("CATIAConstraints")
    ref1 = product.CreateReferenceFromName("Product1/%s.1/!PartBody/%s" % (element1,relation))
    ref2 = product.CreateReferenceFromName("Product1/%s.1/!PartBody/%s" % (element2,relation))
    #1表示偏移拘束
    constraint = constraints.AddBiEltCst(1,ref1,ref2)
    length = constraint.Dimension
    length.value = dist
    constraint.Orientation = 0
    product.Update()
    return True

def test_1(element1,element2,dist,relation):
    catapp = win32.Dispatch("CATIA.Application")
    productdoc = catapp.ActiveDocument
    product = productdoc.Product
    product = product.ReferenceProduct
    constraints1 = product.Connections("CATIAConstraints")
    ref1 = product.CreateReferenceFromName("Product1/%s.1/!PartBody/%s" % (element1,relation))
    ref2 = product.CreateReferenceFromName("Product1/%s.1/!PartBody/%s" % (element2,relation))
    constraint1 = constraints1.AddBiEltCst(2, ref1,ref2)
    constraint1.Orientation = 0
    product.Update()
    return True

def show(item):
    catapp = win32.Dispatch("CATIA.Application")
    productdoc = catapp.ActiveDocument
    product = productdoc.Product
    products1 = product.Products
    product2 = products1.Item("%s" % item)
    product2.ActivateDefaultShape()


class set_CATIA_workbench_env:
    def __init__(self):
        # self.catapp = win32.Dispatch("CATIA.Application")
        self.env_name = {'Part_Design': 'PrtCfg', 'Product_Assembly': 'Assembly',
                'Generative_Sheetmetal_Design': 'SmdNewDesignWorkbench', 'Drafting': 'Drw'}
    def Part_Design(self):
        catapp = win32.Dispatch("CATIA.Application")
        catapp.StartWorkbench(self.env_name[self.Part_Design.__name__])
        try:
            temp = catapp.ActiveDocument
            temp.close()
        except:
            pass
        return
    def Product_Assembly(self):
        catapp = win32.Dispatch("CATIA.Application")
        catapp.StartWorkbench(self.env_name[self.Product_Assembly.__name__])
        try:
            temp = catapp.ActiveDocument
            temp.close()
        except:
            pass
        return
    def Generative_Sheetmetal_Design(self):
        catapp = win32.Dispatch("CATIA.Application")
        catapp.StartWorkbench(self.env_name[self.Generative_Sheetmetal_Design.__name__])
        try:
            temp = catapp.ActiveDocument
            temp.close()
        except:
            pass
        return
    def Drafting(self):
        catapp = win32.Dispatch("CATIA.Application")
        catapp.StartWorkbench(self.env_name[self.Drafting.__name__])
        try:
            temp = catapp.ActiveDocument
            temp.close()
        except:
            pass
        return
#------------------------------------------------------------------------------------------------------執行

# #抓part名稱
# catia_save = ['top','right','following','left']
# small_catia_save = ['small_top','small_left','small_right','small_following']#名稱再來修訂吧3457 小玻璃架
# small2_catia_save = ['small2_following','small2_left','small2_top','small2_right']#名稱再來修訂吧.1235 小玻璃架
#
#  #if save_dir != []:
#
#  #else:
#     #tk.messagebox.showinfo('ATTENTION', 'No Output Directory has set, System will set output directory to Desktop', parent=self.master)
#     #gvar.full_save_dir = mprog.save_dir(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
#     #print(gvar.full_save_dir,type(gvar.full_save_dir))
#
#
# #缺註解
# system_root=os.path.dirname(os.path.realpath(__file__))
# print(system_root)
# #缺註解
# env = set_CATIA_workbench_env()
# env.Generative_Sheetmetal_Design()
#
# # 執行式-open資料夾內的following檔案'
# part_open("following", system_root+"\\big_window")
# #抓出parameter內的數值針對'width'做改變
# Sideplate_param_change("width", gvar.width)
# part_open("left", system_root+"\\big_window")
# Sideplate_param_change("height", gvar.height)
# part_open("right", system_root+"\\big_window")
# Sideplate_param_change("height", gvar.height)
# part_open("top", system_root+"\\big_window")
# Sideplate_param_change("width", gvar.width)
# #新增資料夾路徑
# full_save_dir = save_dir('C:\\Users\\PDAL-BM-1\\Desktop')
# #新增資料夾名稱
# print("%s" % full_save_dir)
# #迴圈存檔
# for item in catia_save:
#     saveas_close(full_save_dir, item, '.CATPart')
#
# #part_open( "Product3", system_root+"\\big_window")
#
# #組立
# open_assembly()
# assembly_open_file(full_save_dir, "following", 0)
# assembly_open_file(full_save_dir, "left", 0)
# assembly_open_file(full_save_dir, "right", 0)
# assembly_open_file(full_save_dir, "top", 0)
# #save不太確定有沒有存到
# saveas_specify_target(full_save_dir,"following",'CATPart')
# saveas_specify_target(full_save_dir,"left",'CATPart')
# saveas_specify_target(full_save_dir,"right",'CATPart')
# saveas_specify_target(full_save_dir,"top",'CATPart')
#
#
# #閃亮小燈泡
# show("following.1")
# show("left.1")
# show("right.1")
# show("top.1")
# #組立偏移(原點座標去坐函數偏移)
# add_offset_assembly("left","top",gvar.width,"yz plane") #偏移組合(零件一,零件二,距離,元素)
# add_offset_assembly("left","top",-gvar.height+300,"xy plane")
# add_offset_assembly("left","top",0,"zx plane")
# add_offset_assembly("right","top",-gvar.width,"yz plane")
# add_offset_assembly("right","top",-gvar.height+300,"xy plane")
# add_offset_assembly("right","top",0,"zx plane")
# add_offset_assembly("following","top",0,"yz plane")
# add_offset_assembly("following","top",(-2*gvar.height)+45,"xy plane")
# add_offset_assembly("following","top",0,"zx plane")
#
# # test_1("Part2","top",1,"right_plane") #偏移組合(零件一,零件二,距離,元素)
# # test_1("Part2","top",0,"under_plane")
# # test_1("Part2","top",0,"back_plane")
# # add_offset_assembly('part2','top',0,'yz plane')
# # add_offset_assembly("Part2","top',0 plane")
#
# saveas(full_save_dir, 'Product', '.CATProduct')
# print('Saved as CATProduct...')
#
# # ------------------------------------------------------------------------------------smallwindow1(有把手的那個)
#
# part_open("small_top", system_root+"\\smalll_window")
# Sideplate_param_change("height", gvar.small_height)#172.5
# part_open("small_left", system_root+"\\smalll_window")
# Sideplate_param_change("width", gvar.small_width)#255
# part_open("small_right", system_root+"\\smalll_window")
# Sideplate_param_change("width", gvar.small_width)#255
# part_open("small_following", system_root+"\\smalll_window")
# Sideplate_param_change("height", gvar.small_height)#172.5
# full_save_dir = save_dir('C:\\Users\\PDAL-BM-1\\Desktop')
# print("%s" % full_save_dir)
# for item in small_catia_save:
#     saveas_close(full_save_dir, item, '.CATPart')
# open_assembly()
#
# assembly_open_file(full_save_dir, "small_top", 0)
# assembly_open_file(full_save_dir, "small_left", 0)
# assembly_open_file(full_save_dir, "small_right", 0)
# assembly_open_file(full_save_dir, "small_following", 0)
#
# saveas_specify_target(full_save_dir,"small_top",'CATPart')
# saveas_specify_target(full_save_dir,"small_left",'CATPart')
# saveas_specify_target(full_save_dir,"small_right",'CATPart')
# saveas_specify_target(full_save_dir,"small_following",'CATPart')
# show("Part3.1")
# show("Part4.1")
# show("Part8.1")
# show("Part9.1")
# add_offset_assembly("Part3","Part9",(-gvar.small_width*2)+50.99+10.105,"xy plane") #偏移組合(零件一,零件二,距離,元素)
# add_offset_assembly("Part3","Part9",0,"yz plane")
# add_offset_assembly("Part3","Part9",0,"zx plane")
# add_offset_assembly("Part9","Part4",gvar.small_height,"yz plane")#變數.一半的h
# add_offset_assembly("Part9","Part4",gvar.small_width-12.69,"xy plane")#變數.w-12.69
# add_offset_assembly("Part9","Part4",0,"zx plane")
# add_offset_assembly("Part4","Part8",-gvar.small_height*2,"yz plane")#變數
# add_offset_assembly("Part4","Part8",0,"xy plane")
# add_offset_assembly("Part4","Part8",0,"zx plane")
# saveas(full_save_dir, 'Product1', '.CATProduct')
# print('Saved as CATProduct...')
#
# #------------------------------------------------------------------------------------smallwindow2(沒把手的那個)
#
# part_open("small2_following", system_root+"\\small2_window")
# Sideplate_param_change("height", gvar.small_height)#height343
# part_open("small2_left", system_root+"\\small2_window")
# Sideplate_param_change("width", gvar.small2_width)#width267.5
# part_open("small2_top", system_root+"\\small2_window")
# Sideplate_param_change("height", gvar.small_height)#height343
# part_open("small2_right", system_root+"\\small2_window")
# Sideplate_param_change("width", gvar.small2_width)#width267.5
# full_save_dir = save_dir('C:\\Users\\PDAL-BM-1\\Desktop')
# print("%s" % full_save_dir)
# for item in small2_catia_save:
#     saveas_close(full_save_dir, item, '.CATPart')
# open_assembly()
# assembly_open_file(full_save_dir, "small2_following", 0)
# assembly_open_file(full_save_dir, "small2_left", 0)
# assembly_open_file(full_save_dir, "small2_top", 0)
# assembly_open_file(full_save_dir, "small2_right", 0)
# saveas_specify_target(full_save_dir,"small2_following",'CATPart')
# saveas_specify_target(full_save_dir,"small2_left",'CATPart')
# saveas_specify_target(full_save_dir,"small2_top",'CATPart')
# saveas_specify_target(full_save_dir,"small2_right",'CATPart')
# show("Part1.1")#更訂patt名稱
# show("Part2.1")#更訂patt名稱
# show("Part3.1")#更訂patt名稱
# show("Part5.1")#更訂patt名稱
# add_offset_assembly("Part3","Part1",-gvar.small2_width*2+48,"xy plane")#變數.
# add_offset_assembly("Part1","Part3",0,"yz plane")
# add_offset_assembly("Part1","Part3",0,"zx plane")
# add_offset_assembly("Part2","Part1",gvar.small_height,"yz plane")#變數.
# add_offset_assembly("Part2","Part1",-gvar.small2_width,"xy plane")#變數.
# add_offset_assembly("Part2","Part1",0,"zx plane")
# add_offset_assembly("Part5","Part1",-gvar.small_height,"yz plane")#變數.
# add_offset_assembly("Part5","Part1",-gvar.small2_width,"xy plane")
# add_offset_assembly("Part5","Part1",0,"zx plane")
# saveas(full_save_dir, 'Product2', '.CATProduct')
# print('Saved as CATProduct...')
#
#
#
#













#












