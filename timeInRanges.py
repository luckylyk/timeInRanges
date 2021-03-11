import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx


PLUGIN_ID = om.MTypeId(0x005599)
NODENAME = "timeInRanges"

RANGES_ATTRIBUTE_NAME = "ranges"
RANGES_ATTRIBUTE_SHORTNAME = "r"
START_FRAME_ATTRIBUTE_NAME = "startFrame"
START_FRAME_ATTRIBUTE_SHORTNAME = "sf"
END_FRAME_ATTRIBUTE_NAME = "endFrame"
END_FRAME_ATTRIBUTE_SHORTNAME = "ef"
OUTPUT_ATTRIBUTE_NAME = "output"
OUTPUT_ATTRIBUTE_SHORTNAME = "o"
TIME_ATTRIBUTE_NAME = "time"
TIME_ATTRIBUTE_SHORTNAME = "t"


class TimeInRanges(ompx.MPxNode):
    def compute(self, mplug, mdatablock):
        print mplug.name(), " evaluated"
        if mplug != TimeInRanges.output:
            return
        output = om.MPlug(self.thisMObject(), TimeInRanges.output)
        out_handle = mdatablock.outputValue(output)
        enable_plug = om.MPlug(self.thisMObject(), TimeInRanges.enable)
        enable_handle = mdatablock.inputValue(enable_plug)
        enable = enable_handle.asBool()
        if enable is False:
            out_handle.setBool(True)
            out_handle.setClean()
            return

        timeplug = om.MPlug(mplug.node(), TimeInRanges.time)
        handle = mdatablock.inputValue(timeplug)
        timevalue = handle.asTime()

        ranges_plug = om.MPlug(self.thisMObject(), TimeInRanges.ranges)
        for i in range(ranges_plug.numElements()):
            child = ranges_plug.elementByLogicalIndex(i)
            start_frame_plug = child.child(0)
            start_frame_handle = mdatablock.inputValue(start_frame_plug)
            start_frame = start_frame_handle.asTime()
            end_frame_plug = child.child(1)
            end_frame_handle = mdatablock.inputValue(end_frame_plug)
            end_frame = end_frame_handle.asTime()
            if start_frame < timevalue < end_frame:
                out_handle.setBool(True)
                out_handle.setClean()
                return
        out_handle.setBool(False)
        out_handle.setClean()


def node_initializer():
    numeric_fn = om.MFnNumericAttribute()
    compound_fn = om.MFnCompoundAttribute()
    unit_fn = om.MFnUnitAttribute()

    TimeInRanges.enable = numeric_fn.create(
        "enable", "e", om.MFnNumericData.kBoolean)
    numeric_fn.setDefault(True)
    numeric_fn.setConnectable(True)
    numeric_fn.setWritable(True)
    numeric_fn.setStorable(True)
    numeric_fn.setReadable(False)
    TimeInRanges.addAttribute(TimeInRanges.enable)

    TimeInRanges.ranges = compound_fn.create(
        RANGES_ATTRIBUTE_NAME, RANGES_ATTRIBUTE_SHORTNAME)

    TimeInRanges.start_frame = unit_fn.create(
        START_FRAME_ATTRIBUTE_NAME, START_FRAME_ATTRIBUTE_SHORTNAME,
        om.MFnUnitAttribute.kTime)
    unit_fn.setConnectable(True)
    unit_fn.setWritable(True)
    unit_fn.setStorable(True)
    unit_fn.setReadable(False)
    compound_fn.addChild(TimeInRanges.start_frame)

    TimeInRanges.end_frame = unit_fn.create(
        END_FRAME_ATTRIBUTE_NAME, END_FRAME_ATTRIBUTE_SHORTNAME,
        om.MFnUnitAttribute.kTime)
    unit_fn.setConnectable(True)
    unit_fn.setWritable(True)
    unit_fn.setStorable(True)
    unit_fn.setReadable(False)
    compound_fn.addChild(TimeInRanges.end_frame)

    compound_fn.setArray(True)
    TimeInRanges.addAttribute(TimeInRanges.ranges)

    TimeInRanges.output = numeric_fn.create(
        OUTPUT_ATTRIBUTE_NAME, OUTPUT_ATTRIBUTE_SHORTNAME,
        om.MFnNumericData.kBoolean)
    numeric_fn.setConnectable(True)
    numeric_fn.setWritable(False)
    numeric_fn.setStorable(True)
    numeric_fn.setReadable(True)
    TimeInRanges.addAttribute(TimeInRanges.output)

    TimeInRanges.time = unit_fn.create(
        TIME_ATTRIBUTE_NAME, TIME_ATTRIBUTE_SHORTNAME,
        om.MFnUnitAttribute.kTime)
    unit_fn.setWritable(True)
    TimeInRanges.addAttribute(TimeInRanges.time)

    TimeInRanges.attributeAffects(
        TimeInRanges.ranges, TimeInRanges.output)
    TimeInRanges.attributeAffects(
        TimeInRanges.time, TimeInRanges.output)
    TimeInRanges.attributeAffects(
        TimeInRanges.enable, TimeInRanges.output)
    TimeInRanges.attributeAffects(
        TimeInRanges.start_frame, TimeInRanges.output)
    TimeInRanges.attributeAffects(
        TimeInRanges.end_frame, TimeInRanges.output)


def node_creator():
    return ompx.asMPxPtr(TimeInRanges())


def initializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject)
    mplugin.registerNode(NODENAME, PLUGIN_ID, node_creator, node_initializer)
    print("switcher loaded")


def uninitializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject)
    mplugin.deregisterNode(PLUGIN_ID)
    print("switcher unloaded")