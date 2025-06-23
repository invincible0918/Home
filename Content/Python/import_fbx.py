import unreal
    
def reimport_fbx_as_static_mesh(fbx_path, destination_path):
    """
    重新导入 FBX 并强制转为 Static Mesh
    :param fbx_path: FBX 文件路径（如 "C:/MyFBX/Character.fbx"）
    :param destination_path: 导入到 UE 的内容目录（如 "/Game/MyFolder/"）
    """
    # 加载 Asset Tools
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    # 设置导入任务
    import_task = unreal.AssetImportTask()
    import_task.filename = fbx_path
    import_task.destination_path = destination_path
    import_task.replace_existing = True  # 覆盖现有资源
    import_task.automated = True  # 静默模式（不弹窗）
    import_task.save = True  # 导入后自动保存
    
    # 配置 FBX 导入选项（强制 Static Mesh）
    fbx_options = unreal.FbxImportUI()
    fbx_options.import_mesh = True
    fbx_options.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH  # 关键：强制 Static Mesh
    fbx_options.static_mesh_import_data.combine_meshes = False  # 不合并 Mesh
    fbx_options.static_mesh_import_data.generate_lightmap_u_vs = True  # 生成光照 UV（可选）
    
    import_task.options = fbx_options
    
    # 执行导入
    asset_tools.import_asset_tasks([import_task])
    unreal.log(f"Reimported {fbx_path} as Static Mesh to {destination_path}")


# 使用示例
reimport_fbx_as_static_mesh("C:/Users/mowl/Documents/Unreal Projects/Home/Content/SourceAssets/home.fbx", "/Game/LevelPrototyping/Meshes/Home")

# exec(open("C:/Users/mowl/Documents/Unreal Projects/Home/Content/Python/import_fbx.py").read())