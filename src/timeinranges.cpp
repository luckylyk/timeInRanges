
#include <maya/MDataHandle.h>
#include <maya/MPlug.h>
#include <maya/MFnPlugin.h>
#include <maya/MTime.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnNumericData.h>
#include <maya/MGlobal.h>
#include "timeinranges.h"
#include <string>

MTypeId TimeInRanges::id(0x00005456);
MObject TimeInRanges::disable;
MObject TimeInRanges::ranges;
MObject TimeInRanges::startFrame;
MObject TimeInRanges::endFrame;
MObject TimeInRanges::output;
MObject TimeInRanges::time;

TimeInRanges::TimeInRanges() {}
TimeInRanges::~TimeInRanges() {}
void* TimeInRanges::creator() {return new TimeInRanges();}


MStatus TimeInRanges::compute(const MPlug & plug, MDataBlock & dataBlock) {
    if (plug != output) {
        return MS::kUnknownParameter;
    }
    MDataHandle outHandle = dataBlock.outputValue(this->output);
    MDataHandle disableHandle = dataBlock.inputValue(this->disable);
    bool isDisable = disableHandle.asBool();
    if (isDisable == true) {
        outHandle.setBool(true);
        outHandle.setClean();
        return MS::kSuccess;
    }
    MDataHandle timeHandle = dataBlock.inputValue(this->time);
    MTime currentTime = timeHandle.asTime();

    MArrayDataHandle rangesArrayHandle = dataBlock.inputArrayValue(this->ranges);
    for (unsigned int i(0); i < rangesArrayHandle.elementCount(); ++i) {
        rangesArrayHandle.jumpToArrayElement(i);
        MDataHandle rangeHandle = rangesArrayHandle.inputValue();

        MTime startTime(rangeHandle.child(this->startFrame).asTime());
        MTime endTime(rangeHandle.child(this->endFrame).asTime());

        if (startTime.value() == endTime.value()) {
            continue;
        }

        if (currentTime.value() >= startTime.value() && currentTime.value() <= endTime.value()) {
            outHandle.setBool(true);
            outHandle.setClean();
            return MS::kSuccess;
        }
    }
    outHandle.setBool(false);
    outHandle.setClean();
    return MS::kSuccess;
}


MStatus TimeInRanges::initialize() {
    MStatus status;
    MFnNumericAttribute fnNumAttr;
    MFnCompoundAttribute fnCompoundAttr;
    MFnUnitAttribute fnUnitAttr;

    disable = fnNumAttr.create("disable", "d", MFnNumericData::kBoolean);
    addAttribute(disable);

    startFrame = fnUnitAttr.create("startFrame", "sf", MFnUnitAttribute::kTime);
    fnUnitAttr.setConnectable(true);
    fnUnitAttr.setWritable(true);
    fnUnitAttr.setStorable(false);
    fnUnitAttr.setReadable(false);

    endFrame = fnUnitAttr.create("endFrame", "ef", MFnUnitAttribute::kTime);
    fnUnitAttr.setConnectable(true);
    fnUnitAttr.setWritable(true);
    fnUnitAttr.setStorable(false);
    fnUnitAttr.setReadable(false);

    ranges = fnCompoundAttr.create("ranges", "r");
    fnCompoundAttr.addChild(startFrame);
    fnCompoundAttr.addChild(endFrame);
    fnCompoundAttr.setArray(true);
    addAttribute(ranges);

    output = fnNumAttr.create("output", "o", MFnNumericData::kBoolean);
    fnNumAttr.setConnectable(true);
    fnNumAttr.setWritable(false);
    fnNumAttr.setStorable(true);
    fnNumAttr.setReadable(true);
    addAttribute(output);

    time = fnUnitAttr.create("time", "t", MFnUnitAttribute::kTime);
    fnUnitAttr.setWritable(true);
    fnUnitAttr.setReadable(false);
    addAttribute(time);

    attributeAffects(time, output);
    attributeAffects(ranges, output);
    attributeAffects(startFrame, output);
    attributeAffects(endFrame, output);
    attributeAffects(disable, output);
    return MS::kSuccess;
}


MStatus initializePlugin(MObject object) {
    MStatus status;
    MFnPlugin fnPlugin(object, "timeInRanges", "0.0", "Any");
    status = fnPlugin.registerNode(
        "timeInRanges",
        TimeInRanges::id,
        TimeInRanges::creator,
        TimeInRanges::initialize);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    MGlobal::displayInfo("timeInRanges loaded");
    return status;
}


MStatus uninitializePlugin(MObject object) {
    MStatus status;
    MFnPlugin fnPlugin(object);
    status = fnPlugin.deregisterNode(TimeInRanges::id);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    MGlobal::displayInfo("timeInRanges unloaded");
    return status;
}
