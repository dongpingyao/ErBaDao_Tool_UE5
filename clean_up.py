import unreal
import os

#实例化unreal类
editor_util = unreal.EditorUtilityLibrary()
system_lib = unreal.SystemLibrary()
editor_asset_lib = unreal.EditorAssetLibrary()

#get the select assets

selected_assets = editor_util.get_selected_assets()
num_assets = len(selected_assets)
clearned = 0

#实例化相对路径
parent_dir = "\\Game"

for asset in selected_assets:
    #get the class instance and the clear text name
    asset_name = system_lib.get_object_name(asset)
    asset_class = asset.get_class()
    class_name = system_lib.get_class_display_name(asset_class)

    new_path = os.path.join(parent_dir, class_name, asset_name)


    unreal.log("Asset {} with class {}".format(asset_name,class_name))