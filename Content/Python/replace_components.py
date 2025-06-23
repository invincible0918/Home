import unreal

def replace_scene_with_static_mesh_component(blueprint_path):
    """
    将 Blueprint 中的所有 SceneComponent 替换为 StaticMeshComponent
    :param blueprint_path: Blueprint 资产路径（如 "/Game/MyBP.MyBP"）
    """
    # 安全加载 Blueprint
    try:
        blueprint = unreal.load_asset(blueprint_path)
        if not blueprint or not isinstance(blueprint, unreal.Blueprint):
            unreal.log_error(f"无效的Blueprint路径或类型: {blueprint_path}")
            return
        unreal.log(f"成功加载Blueprint: {blueprint_path}")
    except Exception as e:
        unreal.log_error(f"加载Blueprint失败: {str(e)}")
        return

    # 获取组件数据
    try:
        subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
        if not subsystem:
            unreal.log_error("无法获取SubobjectDataSubsystem")
            return
            
        subobject_handles = subsystem.k2_gather_subobject_data_for_blueprint(blueprint)
        if not subobject_handles:
            unreal.log_warning(f"Blueprint没有可替换的组件: {blueprint_path}")
            return

        # 打开蓝图编辑器
        editor_subsystem = unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
        editor_subsystem.open_editor_for_assets([blueprint])

        # 处理每个组件
        for handle in subobject_handles:
            component_name = "未知组件"  # 默认值
            try:
                # 安全获取组件
                component = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(handle)
                if not component:
                    continue
                    
                component_name = component.get_name()
                if not isinstance(component, unreal.SceneComponent):
                    unreal.log(f"跳过非SceneComponent: {component_name}")
                    continue

                unreal.log(f"开始处理组件: {component_name}")

                # 记录属性
                transform = component.get_relative_transform()
                attach_parent = component.get_attach_parent()
                socket_name = component.get_attach_socket_name()

                # 创建新组件
                new_component_name = f"{component_name}_Replaced"
                new_component = unreal.EditorLevelLibrary.add_component_to_blueprint(
                    blueprint,
                    unreal.StaticMeshComponent.static_class(),
                    new_component_name
                )

                if not new_component:
                    unreal.log_error(f"创建新组件失败: {new_component_name}")
                    continue

                # 迁移属性
                new_component.set_relative_transform(transform)
                if attach_parent:
                    new_component.attach_to_component(
                        attach_parent,
                        socket_name,
                        unreal.AttachmentRule.KEEP_WORLD,
                        unreal.AttachmentRule.KEEP_WORLD,
                        unreal.AttachmentRule.KEEP_WORLD
                    )

                # 迁移StaticMesh
                if hasattr(component, "static_mesh"):
                    static_mesh = component.static_mesh
                    if static_mesh and isinstance(static_mesh, unreal.StaticMesh):
                        new_component.set_static_mesh(static_mesh)
                        unreal.log(f"迁移StaticMesh: {static_mesh.get_name()}")

                # 删除原组件
                unreal.EditorLevelLibrary.remove_component_from_blueprint(blueprint, component)
                unreal.log(f"成功替换组件: {component_name}")

            except Exception as e:
                unreal.log_error(f"处理组件 {component_name} 时出错: {str(e)}")
                continue

        # 保存蓝图
        unreal.EditorAssetLibrary.save_loaded_asset(blueprint)
        unreal.log(f"Blueprint更新完成: {blueprint_path}")

    except Exception as e:
        unreal.log_error(f"处理Blueprint时发生严重错误: {str(e)}")
        if 'component_name' in locals():
            unreal.log_error(f"最后处理的组件: {component_name}")
        else:
            unreal.log_error("错误发生在初始化阶段")

	
	
# 使用示例
replace_scene_with_static_mesh_component("/Game/LevelPrototyping/Meshes/Home/FbxScene_home.FbxScene_home")

# exec(open("C:/Users/mowl/Documents/Unreal Projects/Home/Content/Python/replace_components.py").read())