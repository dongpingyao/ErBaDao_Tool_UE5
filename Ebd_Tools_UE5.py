# -*- coding: UTF-8 -*-#
import os
import sys
import random
import shutil

for i in sys.path:
    if "ErBaDao_Tool_UE5" in i:
        ErBaDaoPath = True
        UIFile = i + "/ui/Ebd_Tools_maya.ui"
        break
    else:
        for i in sys.path:
            if os.path.exists(i + r"/ErBaDao_Tool_UE5-main"):
                sys.path.append(i + r"/ErBaDao_Tool_UE5-main")
                sys.path.append(i + r"/ErBaDao_Tool_UE5-main/Lib/site_packages")
                UIFile = i + r"/ErBaDao_Tool_UE5-main/ui/Ebd_Tools_UE5.ui"
            else:
                pass
        pass


import unreal
import wget
import zipfile2 as zipfile
import webbrowser as web
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
#实例化 unreal中类的命名
editor_Actor_Sub = unreal.EditorActorSubsystem()
Sys_lib = unreal.SystemLibrary
Math_lib = unreal.MathLibrary

class EbdToolsUe(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(EbdToolsUe, self).__init__(parent)

        #创建ui
        self.widget = QUiLoader().load(r"E:\WORK\UE5\Ebd_Tools_UE5\Python\ui\Ebd_Tools_UE5.ui")
        #绑定我的父窗口
        self.widget.setParent(self)
        self.setCentralWidget(self.widget)
        self.setWindowTitle(self.widget.windowTitle())
        self.create_connections()

     #建立按及获取gui交互信息
    def create_connections(self):
        self.widget.RandomSelectButton.clicked.connect(self.RandomSelect)
        self.widget.RandomRotateButton.clicked.connect(self.RandomRotateSelect)
        # self.widget.RandomSizeButton.clicked.connect(self.RandomSizeSelect)
        # self.widget.RandomOffestButton.clicked.connect(self.RandomOffestSelect)

        self.widget.UpdateButton.clicked.connect(self.Upadate)



    #建立功能函数



    #随机选择actor
    def RandomSelect(self):
        AllSelectedActors = editor_Actor_Sub.get_selected_level_actors()
        if int (self.widget.SendRandomValue.value()) / 100 == 0:
            unreal.log_warning('您的随机选择值为0,请您重新设置')
        elif len(AllSelectedActors) == 0:
            unreal.log_warning('您选择actor为0,请选择后重新执行')
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
        actors_to_select.extend(random_Selected_actors)
        editor_Actor_Sub.set_selected_level_actors(actors_to_select)

    #随机旋转所选actor
    def RandomRotateSelect(self):
        AllSelectedActors = editor_Actor_Sub.get_selected_level_actors()
        RandomRotateMinX_Value = round(self.widget.SendRandomRotateMinX_Value.value(), 2)
        RandomRotateMaxX_Value = round(self.widget.SendRandomRotateMinX_Value.value(), 2)
        RandomRotateMinY_Value = round(self.widget.SendRandomRotateMinX_Value.value(), 2)
        RandomRotateMaxY_Value = round(self.widget.SendRandomRotateMinX_Value.value(), 2)
        RandomRotateMinZ_Value = round(self.widget.SendRandomRotateMinX_Value.value(), 2)
        RandomRotateMaxZ_Value = round(self.widget.SendRandomRotateMinX_Value.value(), 2)
        if len(AllSelectedActors) == 0:
            unreal.log_warning('您选择actor为0,请选择后重新执行')

        for i in AllSelectedActors:
            RandomRotateX_Value = round(random.uniform(RandomRotateMinX_Value, RandomRotateMaxX_Value), 2)
            RandomRotateY_Value = round(random.uniform(RandomRotateMinX_Value, RandomRotateMaxX_Value), 2)
            RandomRotateZ_Value = round(random.uniform(RandomRotateMinX_Value, RandomRotateMaxX_Value), 2)
            RandomVector_Value = (RandomRotateX_Value, RandomRotateY_Value, RandomRotateZ_Value)
            i.add_actor_local_rotation(RandomVector_Value, True, False)

    #下载更新插件函数

    def Upadate(self):
        for i in sys.path:
            if "ErBaDao_Tool_UE5-main" in i:
                scriptPath = i.split(r'ErBaDao_Tool_UE5-main')[0]

        url = "https://codeload.github.com/dongpingyao/ErBaDao_Tool_UE5/zip/refs/heads/main"

        filePath = scriptPath + "ebdTemp"
        fileName = filePath + r'/ErBaDao_Tool_UE5-main.zip'
        fileName2 = filePath + r'/ErBaDao_Tool_UE5-main.zip'
        tarfile = scriptPath
        if os.path.exists(filePath):
            shutil.rmtree(filePath)
            os.makedirs(filePath)
        else:
            os.makedirs(filePath)
        print(u"正在下载中,请稍等...")
        # self.widget.EbdLog_Browser.append("正在下载中,请稍等...")
        # self.widget.EbdLog_Browser.ensureCursorVisible()
        wget.download(url, filePath)
        print(u"下载完成,准备更新")
        # self.widget.EbdLog_Browser.append("下载完成,准备更新")
        # self.widget.EbdLog_Browser.ensureCursorVisible()


        if os.path.exists(scriptPath + r"/ErBaDao_Tool_Maya"):
            shutil.rmtree(scriptPath + r"/ErBaDao_Tool_Maya", ignore_errors=1)

            try:
                zip = zipfile.ZipFile(fileName)
            except:
                zip = zipfile.ZipFile(fileName2)
            zip.extractall(scriptPath + "ebdTemp")
            zip.close()


            for root, dirs, files in os.walk(scriptPath + "ebdTemp" + r"/ErBaDao_Tool_Maya"):
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
            print(u"更新完成")
            # self.widget.EbdLog_Browser.append(u"更新完成")
            # self.widget.EbdLog_Browser.ensureCursorVisible()



# 创建实例化窗口UI
app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
main_windows = EbdToolsUe()
main_windows.show()
unreal.parent_external_window_to_slate(main_windows.winId())


