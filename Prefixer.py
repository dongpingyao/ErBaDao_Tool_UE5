import unreal

#实例化 unreal的类
editor_util = unreal.EditorUtilityLibrary()
system_lib = unreal.SystemLibrary()

#prefix_mapping
prefix_mapping = {
    "Blueprint": "BP_",
    "StatichMesh": "SM_",
    "Material": "M_",
    "MaterialInstanceonstant": "MI_",
    "MaterialFunction": "MF_",
    "ParticleSystem": "PS_",
    "SoundCue": "SC_",
    "SoundWave": "S_",
    "Texture2D": "T_",
    "WidgetBlueprint": "WBP_",
    "MorphTarget": "MT_",
    "SkeletalMesh": "SK_",
    "RenderTarget": "RT_",
    "TextureRenderTarget2D": "TRT_",
    "MediaPlayer": "MP_"
}

#get the selected assets
selected_assets = editor_util.get_selected_assets()
num_assets = len(selected_assets)
prefixed = 0

for asset in selected_assets:
    #获取类实例并且清理文本名字
    asset_name = system_lib.get_object_name(asset)
    asset_class = asset.get_class()
    class_name = system_lib.get_class_display_name(asset_class)

    #赋予所选物体前缀
    class_prefix = prefix_mapping.get(class_name, None)

    if class_prefix is None:
        unreal.log_warning("No mapping for asset {} of type {}".format(asset_name, class_name))
        continue

    #判断选中资产名是否以 设定的前缀名开头,如果不是那么将指定类型的前缀添加到 名称钱
    if not asset_name.startswith(class_prefix):
        #重命名并添加前缀
        new_name = class_prefix + asset_name
        editor_util.rename_asset(asset, new_name)
        prefixed += 1
        unreal.log("prefixed {} of type {} with {}".format(asset_name, class_name, class_prefix))

    else:
        unreal.log("Asset {} of type {} is already prefixed with {}".format(asset_name, class_name, class_prefix))


unreal.log("Prefixed {} of {} assets".format(prefixed, num_assets))
