import unreal

#实例化类
editor_asset_lib = unreal.EditorAssetLibrary
string_lib = unreal.StringLibrary()

#get all asset in source dir
source_dir = "/Game/"
include_subfolders = True
set_textures = 0

assets = editor_asset_lib.list_assets(source_dir,recursive=include_subfolders)
color_patterns = ['_Metallic', '_Roughness', '_Mask', '_Normal', '_BaseColor', '_Opacity', '_Emission', '_ARMS']

for asset in assets:
     for pattern in color_patterns:
         if string_lib.contains(asset,pattern):
             #设置此Texture的相关参数
             asset_obj = editor_asset_lib.load_asset(asset)
             asset_obj.set_editor_property("sRGB", False)


         unreal.log("setting TC_Masks and turning off sRGB for asset {}".format(asset))
         set_texture +=1
         break
         unreal.log("Checking {} against {}".format(asset,pattern))
