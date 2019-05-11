result = cmds.promptDialog(
                                 title='Anti Anti Jittering',
                                 message='Default: piero_c_grp. \n Enter Name of the grp:',
                                 button=['OK', 'Cancel'],
                                 defaultButton='OK',
                                 cancelButton='Cancel',
                                 dismissString='Cancel')
                                 
if result == 'OK':
        imputCommand = cmds.promptDialog(query=True, text=True)

every_element = cmds.listRelatives(imputCommand, ad=True)

#Esto extrae una lista de todos los skins dentro del grupo seleccionado
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
list_of_multMatrix = [] #Lista donde se guardarán todos los multMax para eliminarlos luego

#Va añadiendo todos los nodos multMatrix a la lista
for i in list_of_skins:
    matrix_of_skin = cmds.listConnections('{}.matrix'.format(i))
    for element in matrix_of_skin:
        list_of_multMatrix.append(element)
list(dict.fromkeys(list_of_multMatrix))
    

#Leerá todos los nodos de skin hasta que el diccionario esté vacio
for _ in list_of_skins:
    dic_connections = {}
     #por cada nodo asocia la conexión de multMatrix con su Joint
    for i in list_of_skins:    
        matrix_list = cmds.listConnections('{}.matrix'.format(i))
        joint_list = cmds.listConnections('{}.influenceColor'.format(i))
        c=0
        for x in matrix_list:
            checker = cmds.objectType(x, i = 'multMatrix')
            if checker == True:
                dic_connections[matrix_list[c]] = joint_list[c]
            else:
                pass
            c+=1
      #El for se romperá cuando la lectura no añada ningun elemento al diccionario
    if not dic_connections:
        break
    else:
        #Aquí conecta el hueso a su respectivo key en el diccionario
        for connections in dic_connections:
            jnt = dic_connections.get(connections)
            connections_temp_list = cmds.listConnections('{}.matrixSum'.format(connections),
                                                          source=False,
                                                          destination=True, 
                                                          plugs=True)[0]
                                                 
            cmds.connectAttr('{}.worldMatrix[0]'.format(jnt),
                                         connections_temp_list,
                                         force=True)


#Elimina los nodos

for iteration in list_of_multMatrix:
    checker = cmds.objExists(iteration)
    if checker == True:
        cmds.delete(iteration)
    else:
        pass
