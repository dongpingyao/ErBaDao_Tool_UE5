import unreal

def rename_assets(search_pattern, replace_pattern,use_case):
    # instance of unreal classes(实例化 unreal的类)
    system_lib = unreal.SystemLibrary()
    editor_util = unreal.EditorUtilityLibrary()
    string_lib = unreal.StringLibrary()

    #get the selected assets (获取选择资产的信息)
    select_assets = editor_util.get_selected_assets()
    num_assets = len(select_assets)
    replaced = 0

    unreal.log("Selectted {} assets".format(num_assets))

    #循环将资产重命名
    for assets in select_assets:
        assetsName = system_lib.get_object_name(assets) #获取指定物体的名称
        # unreal.log(assets_name)
        # 检查资产名是否包含将要替换的文本
        if string_lib.contains(assetsName, search_pattern, use_case=use_case):
            search_case = unreal.SearchCase.CASE_SENSITIVE if use_case else unreal.SearchCase.IGNORE_CASE
            replaced_name = string_lib.replace(assetsName, search_pattern, replace_pattern,search_case=search_case)
            editor_util.rename_asset(assets, replaced_name)

            replaced += 1
            unreal.log("Replaced {} with {}".format(assetsName, replaced_name))
            pass

        else:
            unreal.log("{} didn not match the search pattern, was skipped".format(assetsName))
    unreal.log("Replaced {} of {} assets".format(replaced, num_assets))
rename_assets("HAHA","new",False)