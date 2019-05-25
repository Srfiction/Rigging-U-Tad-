name = 'ble'
side = 'r'
top = cmds.spaceLocator(n='{}TopParent_{}_loc'.format(name, side))[0]
bottom = cmds.spaceLocator(n='{}BottomParent_{}_loc'.format(name, side))[0]
uno = cmds.spaceLocator(n='{}Parent01_{}_loc'.format(name, side))[0]
dos = cmds.spaceLocator(n='{}Parent02_{}_loc'.format(name, side))[0]
tres = cmds.spaceLocator(n='{}Parent03_{}_loc'.format(name, side))[0]


rot_list = []
up_list = []
twist_list= []
for i, n in [top, 'Top'], [bottom, 'Bottom'],  [uno,'01'], [dos, '02'], [tres, '03']:
    up = cmds.duplicate(i, name='{}{}Up_{}_loc'.format(name, n, side))[0]
    rot = cmds.duplicate(i, name='{}{}Rot_{}_loc'.format(name, n, side))[0]
    cmds.parent(up, rot, i)
    twist  = cmds.duplicate(rot, name='{}{}Twist_{}_loc'.format(name, n, side))[0]
    cmds.parent(twist, rot)
    pos = cmds.xform(i, matrix=True, ws=True, q=True)
    jnt = cmds.joint(n='{}_jnt'.format(i))
    cmds.xform(jnt, matrix=pos, ws=True)
    cmds.setAttr('{}.tz'.format(up), 1)
    rot_list.append(rot)
    up_list.append(up)
    twist_list.append(twist)


ai1 = cmds.aimConstraint(bottom, rot_list[2], aimVector = [1,0,0], upVector = [0,0,1], worldUpType='object', worldUpObject=up_list[2])
ai2 = cmds.aimConstraint(bottom, rot_list[3], aimVector = [1,0,0], upVector = [0,0,1], worldUpType='object', worldUpObject=up_list[3])
ai3 = cmds.aimConstraint(bottom, rot_list[4], aimVector = [1,0,0], upVector = [0,0,1], worldUpType='object', worldUpObject=up_list[4])

ai4 = cmds.aimConstraint(bottom, rot_list[0], aimVector = [1,0,0], upVector = [0,0,1], worldUpType='object', worldUpObject=up_list[0])
ai5 = cmds.aimConstraint(top, rot_list[1], aimVector = [-1,0,0], upVector = [0,0,1], worldUpType='object', worldUpObject=up_list[1])


blen1 = cmds.shadingNode('blendColors', au=True, n='parent01_r_blend')
cmds.setAttr('{}.blender'.format(blen1), 0.25)
blen2 = cmds.shadingNode('blendColors', au=True, n='parent02_r_blend')
cmds.setAttr('{}.blender'.format(blen2), 0.5)
blen3 = cmds.shadingNode('blendColors', au=True, n='parent03_r_blend')
cmds.setAttr('{}.blender'.format(blen3), 0.75)

for axisUp, axisLow in ['x', 'R'], ['y','G'], ['z','B']:
    for blen in [blen1, blen2, blen3]:
        cmds.connectAttr('{}.t{}'.format(bottom, axisUp), '{}.color1.color1{}'.format(blen, axisLow))
        cmds.connectAttr('{}.t{}'.format(top, axisUp), '{}.color2.color2{}'.format(blen, axisLow))

    cmds.connectAttr('{}.output{}'.format(blen1, axisLow), '{}.t{}'.format(uno, axisUp))
    cmds.connectAttr('{}.output{}'.format(blen2, axisLow), '{}.t{}'.format(dos, axisUp))
    cmds.connectAttr('{}.output{}'.format(blen3, axisLow), '{}.t{}'.format(tres, axisUp))
    
    

for i, num in [twist_list[2], '1'], [twist_list[3], '2'], [twist_list[4], '3']:
    mult = cmds.shadingNode('multiplyDivide', au=True, n='parent0{}_r_mult'.format(num))
    cmds.connectAttr('{}.rx'.format(bottom), '{}.input1X'.format(mult))
    cmds.connectAttr('{}.outputX'.format(mult), '{}.rx'.format(i))
    if num == '1':
        cmds.setAttr('{}.input2X'.format(mult), 0.25)
    elif num == '2':
        cmds.setAttr('{}.input2X'.format(mult), 0.5)
    else:
        cmds.setAttr('{}.input2X'.format(mult), 0.75)
