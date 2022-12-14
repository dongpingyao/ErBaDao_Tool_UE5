# -*- coding: UTF-8 -*-#
import subprocess, tempfile, os
import sys
import random
import shutil
import json

push = 1
if push == 0:
    ErBaDaoToolsPath = r"E:\WORK\PycharmProjects"
    sys.path.append(ErBaDaoToolsPath + r"\ErBaDao_Tool_UE5")
    sys.path.append(ErBaDaoToolsPath + r"\ErBaDao_Tool_UE5\Lib\site_packages")
    UIFile = ErBaDaoToolsPath + r"\ErBaDao_Tool_UE5\ui\Ebd_Tools_UE5.ui"
    UIFile_UeSeting = ErBaDaoToolsPath + r"\ErBaDao_Tool_UE5\ui\Ebd_Tools_UE5_Seting.ui"
    SetingData = ErBaDaoToolsPath + r"\ErBaDao_Tool_UE5\Path_setting.json"
else:
    for i in sys.path:
        if "ErBaDao_Tool_UE5-main" in i:
            ErBaDaoPath = True
            UIFile = i + r"/ui/Ebd_Tools_UE5.ui"
            break
        else:
            ErBaDaoPath = False

    if ErBaDaoPath == False:
        for i in sys.path:
            if "Plugins" in i:
                ErBaDaoToolsPath = i.split("Plugins")[0] + "Plugins"
                ErBaDaoPath = True
                print(ErBaDaoToolsPath)
                if os.path.exists(ErBaDaoToolsPath + r"/ErBaDao_Tool_UE5-main"):
                    sys.path.append(ErBaDaoToolsPath + r"/ErBaDao_Tool_UE5-main")
                    sys.path.append(ErBaDaoToolsPath + r"/ErBaDao_Tool_UE5-main\Lib\site_packages")
                    UIFile = ErBaDaoToolsPath + r"/ErBaDao_Tool_UE5-main\ui\Ebd_Tools_UE5.ui"
                    UIFile_UeSeting = ErBaDaoToolsPath + r"\ErBaDao_Tool_UE5\ui\Ebd_Tools_UE5_Seting.ui"
                    SetingData = ErBaDaoToolsPath + r"\ErBaDao_Tool_UE5\Path_setting.json"
                else:
                    pass
                break
            else:
                pass


import unreal
import wget
import zipfile39 as zipfile
import webbrowser as web
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
#实例化 unreal中类的命名
editor_Actor_Sub = unreal.EditorActorSubsystem()
Sys_lib = unreal.SystemLibrary
Math_lib = unreal.MathLibrary

#创建主窗口所有内容
class EbdToolsUe(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(EbdToolsUe, self).__init__(parent)

        #创建ui
        self.widget = QUiLoader().load(UIFile)
        #绑定我的父窗口
        self.widget.setParent(self)
        self.setCentralWidget(self.widget)
        self.setWindowTitle(self.widget.windowTitle())
        self.create_connections()

     #建立按及获取gui交互信息
    def create_connections(self):
        # 绑定随机相关的按钮
        self.widget.RandomSelectButton.clicked.connect(self.RandomSelect)
        self.widget.RandomRotateButton.clicked.connect(self.RandomRotateSelect)
        self.widget.RandomSizeButton.clicked.connect(self.RandomSizeSelect)
        self.widget.RandomOffestButton.clicked.connect(self.RandomOffestSelect)

        #绑定rizomUv的按钮
        self.widget.sendToRizom_Button.clicked.connect(self.sendToRizom)
        self.widget.getFromRizom_Button.clicked.connect(self.getFromRizom)

        #绑定更新插件的按钮
        self.widget.UpdateButton.clicked.connect(self.Upadate)

        #绑定跳出子窗口
        self.widget.childShowButton.clicked.connect(self.childShowFun)



    #建立功能函数

    #子窗口弹出
    def childShowFun(self):
        childWindowsApp = None
        if not QtWidgets.QApplication.instance():
            childWindowsApp = QtWidgets.QApplication(sys.argv)
        self.childwindow = EbdToolsUeSeting()
        self.childwindow.show()
        unreal.parent_external_window_to_slate(self.childwindow.winId())

    #随机选择actor
    def RandomSelect(self):
        AllSelectedActors = editor_Actor_Sub.get_selected_level_actors()
        if int (self.widget.SendRandomValue.value()) / 100 == 0:
            unreal.log_warning('Warning:您的随机选择值为0,请您重新设置')
            self.widget.EbdLog_Browser.append("Warning:您的随机选择值为0,请您重新设置")
            self.widget.EbdLog_Browser.ensureCursorVisible()
        elif len(AllSelectedActors) == 0:
            unreal.log_warning('Warning:您选择actor为0,请选择后重新执行')
            self.widget.EbdLog_Browser.append("Warning:您选择actor为0,请选择后重新执行")
            self.widget.EbdLog_Browser.ensureCursorVisible()
        RandomValue = int (self.widget.SendRandomValue.value() / 100 * len(AllSelectedActors))
        random_Selected_actors = []
        actors_to_select = []
        try:
            for i in range(RandomValue):
                randomSingle = random.choice(AllSelectedActors)
                random_Selected_actors.append(randomSingle)
                AllSelectedActors.remove(randomSingle)
        except:
            unreal.log_warning('您选择的actor为0,请检查后再尝试')
            self.widget.EbdLog_Browser.append("warning:您选择actor为0,请选择后重新执行")
            self.widget.EbdLog_Browser.ensureCursorVisible()
        actors_to_select.extend(random_Selected_actors)
        editor_Actor_Sub.set_selected_level_actors(actors_to_select)

    #随机旋转所选actor
    def RandomRotateSelect(self):
        AllSelectedActors = editor_Actor_Sub.get_selected_level_actors()
        RandomRotateMinX_Value = self.widget.SendRandomRotateMinX_Value.value()
        RandomRotateMaxX_Value = self.widget.SendRandomRotateMaxX_Value.value()
        RandomRotateMinY_Value = self.widget.SendRandomRotateMinY_Value.value()
        RandomRotateMaxY_Value = self.widget.SendRandomRotateMaxY_Value.value()
        RandomRotateMinZ_Value = self.widget.SendRandomRotateMinZ_Value.value()
        RandomRotateMaxZ_Value = self.widget.SendRandomRotateMaxZ_Value.value()

        if len(AllSelectedActors) == 0:
            unreal.log_warning('您选择actor为0,请选择后重新执行')
            self.widget.EbdLog_Browser.append("warning:您选择actor为0,请选择后重新执行")
            self.widget.EbdLog_Browser.ensureCursorVisible()

        for i in AllSelectedActors:
            RandomRotateX_Value = random.uniform(RandomRotateMinX_Value, RandomRotateMaxX_Value)
            RandomRotateY_Value = random.uniform(RandomRotateMinY_Value, RandomRotateMaxY_Value)
            RandomRotateZ_Value = random.uniform(RandomRotateMinZ_Value, RandomRotateMaxZ_Value)

            RandomVector_Value = (RandomRotateX_Value, RandomRotateY_Value, RandomRotateZ_Value)
            i.set_actor_rotation(RandomVector_Value, True)

    # 随机缩放所选actor
    def RandomSizeSelect(self):
        AllSelectedActors = editor_Actor_Sub.get_selected_level_actors()
        RandomSizeMinX_Value = self.widget.SendRandomSizeMinX_Value.value()
        RandomSizeMaxX_Value = self.widget.SendRandomSizeMaxX_Value.value()
        RandomSizeMinY_Value = self.widget.SendRandomSizeMinY_Value.value()
        RandomSizeMaxY_Value = self.widget.SendRandomSizeMaxY_Value.value()
        RandomSizeMinZ_Value = self.widget.SendRandomSizeMinZ_Value.value()
        RandomSizeMaxZ_Value = self.widget.SendRandomSizeMaxZ_Value.value()

        if len(AllSelectedActors) == 0:
            unreal.log_warning('您选择actor为0,请选择后重新执行')
            self.widget.EbdLog_Browser.append("warning:您选择actor为0,请选择后重新执行")
            self.widget.EbdLog_Browser.ensureCursorVisible()

        for i in AllSelectedActors:
            aa = str(i.get_actor_scale3d())
            bb = (aa.split("{")[-1].split("}")[0])
            cc = bb.split(" ")
            dd = ((cc[1]+cc[3]+cc[5]).split(","))
            Actor_Scale_Vector = (float(dd[0]),float(dd[1]),float(dd[2]))

            RandomSizeX_Value = random.uniform(RandomSizeMinX_Value, RandomSizeMaxX_Value) + Actor_Scale_Vector[0]
            RandomSizeY_Value = random.uniform(RandomSizeMinY_Value, RandomSizeMaxY_Value) + Actor_Scale_Vector[1]
            RandomSizeZ_Value = random.uniform(RandomSizeMinZ_Value, RandomSizeMaxZ_Value) + Actor_Scale_Vector[2]
            RandomVector_Value = (RandomSizeX_Value, RandomSizeY_Value, RandomSizeZ_Value)
            i.set_actor_scale3d(RandomVector_Value)
    #随机偏移
    def RandomOffestSelect(self):
        AllSelectedActors = editor_Actor_Sub.get_selected_level_actors()
        RandomOffestMinX_Value = self.widget.SendRandomOffestMinX_Value.value()
        RandomOffestMaxX_Value = self.widget.SendRandomOffestMaxX_Value.value()
        RandomOffestMinY_Value = self.widget.SendRandomOffestMinY_Value.value()
        RandomOffestMaxY_Value = self.widget.SendRandomOffestMaxY_Value.value()
        RandomOffestMinZ_Value = self.widget.SendRandomOffestMinZ_Value.value()
        RandomOffestMaxZ_Value = self.widget.SendRandomOffestMaxZ_Value.value()

        if len(AllSelectedActors) == 0:
            unreal.log_warning('您选择actor为0,请选择后重新执行')
            self.widget.EbdLog_Browser.append("warning:您选择actor为0,请选择后重新执行")
            self.widget.EbdLog_Browser.ensureCursorVisible()

        for i in AllSelectedActors:
            RandomOffestX_Value = random.uniform(RandomOffestMinX_Value, RandomOffestMaxX_Value)
            RandomOffestY_Value = random.uniform(RandomOffestMinY_Value, RandomOffestMaxY_Value)
            RandomOffestZ_Value = random.uniform(RandomOffestMinZ_Value, RandomOffestMaxZ_Value)

            RandomVector_Value = (RandomOffestX_Value, RandomOffestY_Value, RandomOffestZ_Value)
            i.add_actor_local_offset(RandomVector_Value, True, False)

    # 发送模型到RizomUv
    def sendToRizom(self):
        actors = unreal.EditorLevelLibrary.get_selected_level_actors()
        static_mesh = actors[0].static_mesh_component.static_mesh

        assetsPathName = static_mesh.get_path_name()
        assetsName = static_mesh.get_name()
        exportFile = tempfile.gettempdir() + r"/Ebd_Temp/" + "EBD_RizomExport.fbx"

        unreal_task = unreal.AssetExportTask()

        unreal_task.automated = True
        unreal_task.filename = exportFile
        unreal_task.object = static_mesh
        unreal_task.replace_identical = True
        unreal_task.prompt = True

        fbx_options = unreal.FbxExportOption()
        fbx_options.collision = False
        fbx_options.ascii = True
        fbx_options.vertex_color = True
        fbx_options.export_morph_targets = True
        fbx_options.map_skeletal_motion_to_root = True
        fbx_options.force_front_x_axis = True
        fbx_options.level_of_detail = False
        unreal_task.options = fbx_options

        unreal.Exporter.run_asset_export_task(unreal_task)

        # 发送到 rizomUV
        with open(SetingData, 'rb') as odlFile_obj:
            params = json.load(odlFile_obj)
            rizomPath = params[0]["rizomPath"]
            odlFile_obj.close()
            print (rizomPath)
        cmd = '"' + rizomPath + '" "' + exportFile + '"'
        subprocess.Popen(cmd)

    # 接收模型到UE5
    def getFromRizom(self):

        actors = unreal.EditorLevelLibrary.get_selected_level_actors()
        static_mesh = actors[0].static_mesh_component.static_mesh

        assetsPathName = static_mesh.get_path_name()
        assetsPath = assetsPathName.split("/" + assetsPathName.split("/")[-1])[0]
        assetsName = static_mesh.get_name()
        importFile = tempfile.gettempdir() + r"/Ebd_Temp/" + "EBD_RizomExport.fbx"

        unreal_import_Task = unreal.AssetImportTask()

        unreal_import_Task.automated = True
        unreal_import_Task.destination_name = assetsName
        unreal_import_Task.destination_path = assetsPath
        unreal_import_Task.filename = importFile
        unreal_import_Task.replace_existing = True
        unreal_import_Task.save = True

        task = [unreal_import_Task]
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(task)

    #下载更新插件函数

    def Upadate(self):
        for i in sys.path:
            if "ErBaDao_Tool_UE5-main" in i:
                scriptPath = i.split(r'ErBaDao_Tool_UE5-main')[0]

        url = "https://codeload.github.com/dongpingyao/ErBaDao_Tool_UE5/zip/refs/heads/main"

        filePath = scriptPath + "ebdTemp"
        fileName = filePath + r'\ErBaDao_Tool_UE5-main.zip'
        tarfile = scriptPath
        if os.path.exists(filePath):
            shutil.rmtree(filePath)
            os.makedirs(filePath)
            pass
        else:
            os.makedirs(filePath)
        unreal.log(u"正在下载中,请稍等...")
        self.widget.EbdLog_Browser.append("正在下载中,请稍等...")
        self.widget.EbdLog_Browser.ensureCursorVisible()
        wget.download(url, filePath)
        unreal.log(u"下载完成,准备更新")
        self.widget.EbdLog_Browser.append("下载完成,准备更新")
        self.widget.EbdLog_Browser.ensureCursorVisible()


        if os.path.exists(scriptPath + r"\ErBaDao_Tool_UE5-main"):
            shutil.rmtree(scriptPath + r"\ErBaDao_Tool_UE5-main", ignore_errors=1)

            try:
                zip = zipfile.ZipFile(fileName)
            except:
                pass
            zip.extractall(scriptPath + "ebdTemp")
            zip.close()


            for root, dirs, files in os.walk(scriptPath + "ebdTemp" + r"\ErBaDao_Tool_UE5-main"):
                for file in files:
                    src_file = os.path.join(root, file).replace('\\', '/')
                    ls = src_file.split(src_file.split("/")[-1])[0][:-1]
                    target_path = ls.split("ebdTemp/")[0] + ls.split("ebdTemp/")[-1]
                    try:
                        os.makedirs(target_path)
                    except:
                        pass
                    try:
                        shutil.copy(src_file, target_path)
                    except:
                        pass
            unreal.log(u"更新完成")
            self.widget.EbdLog_Browser.append(u"更新完成")
            self.widget.EbdLog_Browser.ensureCursorVisible()

#创建子窗口(ue5插件设置)所有内容
class EbdToolsUeSeting(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EbdToolsUeSeting, self).__init__(parent)

        #创建ui
        self.widget = QUiLoader().load(UIFile_UeSeting )
        #绑定我的父窗口
        self.widget.setParent(self)
        self.setWindowTitle(self.widget.windowTitle())
        self.create_connections()
     #建立按及获取gui交互信息
    def create_connections(self):
        # 绑定随机相关的按钮
        self.widget.rizomPath_lineEdit.editingFinished.connect(self.SetingRizomPath)
        self.widget.mayaPath_lineEdit.editingFinished.connect(self.SetingMayaPath)
        self.widget.photoshopPath_lineEdit.editingFinished.connect(self.SetingPsPath)
        self.widget.SubtancePainterPath_lineEdit.editingFinished.connect(self.SetingSpPath)

    #创建设置框显示设置路径函数并运行


    #创建设置rizomUv软件路径函数
    def SetingRizomPath(self):
        with open(SetingData, 'rb') as odlFile_obj:
            params = json.load(odlFile_obj)
            setingPathName = "rizomPath"
            setingPath = self.widget.rizomPath_lineEdit.text()
            params[0][setingPathName] = setingPath
            odlFile_obj.close()
        with open(SetingData, "w", encoding='utf-8') as file_obj:
            json.dump(params, file_obj, indent=2, ensure_ascii=False)
            file_obj.close()
    #创建设置maya软件路径函数
    def SetingMayaPath(self):
        with open(SetingData, 'rb') as odlFile_obj:
            params = json.load(odlFile_obj)
            params[0]["rizomPath"] = r"C:\Program Files\Rizom Lab\RizomUV 2019\rizomuv.exe"
            odlFile_obj.close()
        with open(SetingData, "w", encoding='utf-8') as file_obj:
            json.dump(params, file_obj, indent=2, ensure_ascii=False)
            file_obj.close()
    #创建设置PS软件路径函数
    def SetingPsPath(self):
        with open(SetingData, 'rb') as odlFile_obj:
            params = json.load(odlFile_obj)
            params[0]["rizomPath"] = r"C:\Program Files\Rizom Lab\RizomUV 2019\rizomuv.exe"
            odlFile_obj.close()
        with open(SetingData, "w", encoding='utf-8') as file_obj:
            json.dump(params, file_obj, indent=2, ensure_ascii=False)
            file_obj.close()
    #创建设置SP软件路径函数
    def SetingSpPath(self):
        with open(SetingData, 'rb') as odlFile_obj:
            params = json.load(odlFile_obj)
            params[0]["rizomPath"] = r"C:\Program Files\Rizom Lab\RizomUV 2019\rizomuv.exe"
            odlFile_obj.close()
        with open(SetingData, "w", encoding='utf-8') as file_obj:
            json.dump(params, file_obj, indent=2, ensure_ascii=False)
            file_obj.close()

# 创建实例化窗口主UI



app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
main_windows = EbdToolsUe()
main_windows.show()
unreal.parent_external_window_to_slate(main_windows.winId())


