
muscle = cmds.ls(sl=True)[0]

simMuscle = cmds.duplicate(muscle, n='Sim{}'.format(muscle))[0]

nCloth=cmds.createNode('nCloth', n= '{}_{}_nCloth'.format(muscle.split('_')[0], muscle.split('_')[1]))

cmds.connectAttr('{}Shape.worldMesh[0]'.format(muscle), '{}.inputMesh'.format(nCloth))
cmds.connectAttr('{}Shape.worldMesh[0]'.format(muscle), '{}.restShapeMesh'.format(nCloth))


cmds.connectAttr('nucleus1.startFrame', '{}.startFrame'.format(nCloth))


connectionList = cmds.listConnections('nucleus1.outputObjects')

num = len(connectionList)

cmds.connectAttr('{}.currentState'.format(nCloth), 'nucleus1.inputActive[{}]'.format(num))
cmds.connectAttr('{}.currentState'.format(nCloth), 'nucleus1.inputActiveStart[{}]'.format(num))
cmds.connectAttr('nucleus1.outputObjects[{}]'.format(num), '{}.nextState'.format(nCloth))
cmds.connectAttr('{}.outputMesh'.format(nCloth), '{}Shape.inMesh'.format(simMuscle))
cmds.connectAttr('time1.outTime', '{}.currentTime'.format(nCloth))

