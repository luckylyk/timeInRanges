
from maya import cmds


CONNECTION_TO_TIME_CMD = """cmds.connectAttr("time1.outTime", "{}.time")"""


def set_time_in_ranges_enabled(state):
    for time_in_ranges in cmds.ls(type="timeInRanges"):
        cmds.setAttr(time_in_ranges + ".disable", not state)


def add_node_to_shot_range_visibility(node, shot):
    try:
        visibility = node + ".lodVisibility"
        time_in_ranges = cmds.listConnections(visibility, type="timeInRanges")[0]
    except TypeError:
        # No time in ranges created, then create one.
        time_in_ranges = cmds.createNode("timeInRanges")
        cmds.connectAttr(time_in_ranges + ".output", visibility)
        # We connect the node to the time attribute using an eval deferred
        # to fix an issue in DG evaluation mode.
        # Without eval deferred, the connection to time is not detected as far
        # as the time in range is not selected ... Welcome to the WTF World of
        # Maya.
        cmds.evalDeferred(CONNECTION_TO_TIME_CMD.format(time_in_ranges))
    if shot in (cmds.listConnections(time_in_ranges, type="shot") or []):
        # Node is already connected to time in range.
        return
    index = find_free_ranges_attribute_index(time_in_ranges)
    input_ = time_in_ranges + ".ranges[{}].startFrame".format(index)
    cmds.connectAttr(shot + ".startFrame", input_)
    input_ = time_in_ranges + ".ranges[{}].endFrame".format(index)
    cmds.connectAttr(shot + ".endFrame", input_)
    return time_in_ranges


def remove_node_from_shot_range_visibility(node, shot):
    try:
        attr = node + ".lodVisibility"
        time_in_ranges = cmds.listConnections(attr, type="timeInRanges")[0]
    except TypeError:
        # Shot is not connected to any shot.
        return
    if shot not in (cmds.listConnections(time_in_ranges, type="shot") or []):
        # Shot is not connected to any shot either.
        return
    # Disconnect attributes from shot nodes to time in ranges node.
    for attr in ("startFrame", "endFrame"):
        connections = cmds.listConnections(shot + "." + attr, plugs=True)
        for dst in connections:
            if time_in_ranges not in dst:
                continue
            src = cmds.connectionInfo(dst, sourceFromDestination=True)
            cmds.disconnectAttr(src, dst)
            cmds.setAttr(dst, 0)

    if not cmds.listConnections(time_in_ranges, type="shot"):
        # The timeInRanges node doesn't have any shot connected anymore and
        # can be deleted. The lod visibility then is set to True.
        cmds.delete(time_in_ranges)
        cmds.setAttr(node + ".lodVisibility", True)


def list_shots_connected(node):
    try:
        attr = node + ".lodVisibility"
        time_in_ranges = cmds.listConnection(attr, type="timeInRanges")[0]
    except IndexError:
        # Shot is not connected to any shot.
        return []
    return cmds.listConnections(time_in_ranges, type="shot") or []


def find_free_ranges_attribute_index(time_in_ranges):
    start = time_in_ranges + ".ranges[{}].startFrame"
    end = time_in_ranges + ".ranges[{}].startFrame"
    def index_is_connected(index):
        return (
            cmds.listConnections(start.format(i)) or
            cmds.listConnections(end.format(i)))
    i = 0
    while index_is_connected(i):
        i += 1
    return i


if __name__ == "__main__":
    pcube = cmds.polyCube()[0]
    for sf in (25, 100, 135, 250):
        shot = cmds.shot(startTime=sf, endTime=sf + 25)
        add_node_to_shot_range_visibility(pcube, shot)

    shots = cmds.ls(type="shot")
    remove_node_from_shot_range_visibility(pcube, shots[2])

