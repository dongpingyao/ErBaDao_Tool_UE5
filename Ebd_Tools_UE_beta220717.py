# -*- coding: UTF-8 -*-#
import os
import unreal
import sys
import random
# import math
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





# 创建实例化窗口UI
app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
main_windows = EbdToolsUe()
main_windows.show()
unreal.parent_external_window_to_slate(main_windows.winId())


