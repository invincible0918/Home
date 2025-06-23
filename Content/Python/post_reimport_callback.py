import unreal

def on_asset_post_import(asset):
    """在资源导入完成后触发"""
    if isinstance(asset, unreal.StaticMesh):  # 只处理 StaticMesh
        unreal.log(f"[自动回调] Reimport 完成: {asset.get_name()}")
        # 在这里调用你的后续脚本
        # 例如：修改材质、生成LOD、触发其他工具等
        your_custom_script(asset)

def your_custom_script(static_mesh):
    """你的自定义逻辑"""
    unreal.log(f"处理 StaticMesh: {static_mesh.get_name()}")

# 注册事件监听
unreal.register_slate_post_tick_callback(on_asset_post_import)

# exec(open("C:/Users/mowl/Documents/Unreal Projects/Home/Content/Python/post_reimport_callback.py").read())