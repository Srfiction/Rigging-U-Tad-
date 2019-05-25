list = cmds.ls(sl=True)

for ctr in list:
    grp = cmds.group(em=True, n='{}_zero'.format(ctr))
    pos = cmds.xform(ctr, matrix=True, q=True, ws=True)
    cmds.xform(grp, matrix=pos, ws=True)
    cmds.parent(ctr, grp)
