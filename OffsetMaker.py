list = cmds.ls(sl=True)

for ctr in list:
    prnt = cmds.listRelatives(ctr, p=True)[0]
    grp = cmds.group(em=True, n='{}_zero'.format(ctr))
    pos = cmds.xform(ctr, matrix=True, q=True, ws=True)
    cmds.xform(grp, matrix=pos, ws=True)
    cmds.parent(ctr, grp)
    cmds.parent(grp, prnt)
