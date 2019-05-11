import maya.cmds as cmds
'''
Script de AntiJittering

Para que este script funcione la escena tiene que cumplir ciertas normas de nomenclatura. 

    Las piezas skineadas tienen que tener 'geo' en el nombre
    Los huesos de skin tienen que estar nombrados segun la nomenclatura de Ilion (Ej; upperArm12_l_skn)
'''
result = cmds.promptDialog(
                                 title='Anti Jittering',
                                 message='Default: pieroLayout_c_grp. \n Enter Name of the grp:',
                                 button=['OK', 'Cancel'],
                                 defaultButton='OK',
                                 cancelButton='Cancel',
                                 dismissString='Cancel')
                                 
if result == 'OK':
        imputCommand = cmds.promptDialog(query=True, text=True)
  
def applyJittering(skin_node=None):

    center_ctr = 'center_c_ctr'
    
    joints_list = cmds.skinCluster(skin_node, query=True, influence=True)
    for jnt in joints_list:
        connections_temp_list = cmds.listConnections('{}.worldMatrix[0]'.format(jnt),
                                                     source=False,
                                                     destination=True, 
                                                     plugs=True)
        for conection in connections_temp_list:
            if skin_node in conection:
                skin_conection = conection
                break
                
        if skin_conection:
            joint_name = jnt.split('_')[0]
            side = jnt.split('_')[1]
            joint_usage = jnt.split('_')[2]
            
            center_name = jnt.split('_')[0]
            center_usage = jnt.split('_')[2]
            
            mult_mat = '{}{}InverseMatrix{}{}_{}_multmat'.format(joint_name, 
                                                                 joint_usage.capitalize(), 
                                                                 center_name.capitalize(), 
                                                                 center_usage.capitalize(), 
                                                                 side)
            
            #in case that multMAtrix node does not exist (create it and make input connections)
            if not cmds.objExists(mult_mat):
                mult_mat = cmds.createNode('multMatrix', name=mult_mat)
                cmds.connectAttr('{}.worldMatrix[0]'.format(jnt),
                                 '{}.matrixIn[0]'.format(mult_mat))
                cmds.connectAttr('{}.worldInverseMatrix[0]'.format(center_ctr),
                                 '{}.matrixIn[1]'.format(mult_mat))                
            cmds.connectAttr('{}.matrixSum'.format(mult_mat),
                             skin_conection,
                             force=True)


#CONSEGUIR LOS SKINS DENTRO DE UN GRUPO
every_element = cmds.listRelatives(imputCommand, ad=True)

list_of_skins = []
for element in every_element:
    if 'geo' not in element:
        pass
    else: 
        list_of_connections = cmds.listConnections(element)
        
        if list_of_connections == None:
            pass
        else:
            for connection in list_of_connections:
                checker = cmds.objectType(connection, i = 'skinCluster')
                if checker == True:
                    print connection
                    list_of_skins.append(connection)
                else:
                    pass
list_of_skins = list(dict.fromkeys(list_of_skins))
#################################################################
for i in list_of_skins:
    applyJittering(skin_node=i)

cmds.parentConstraint('center_c_ctr', imputCommand)
