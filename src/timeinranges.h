#include <maya/MPxNode.h>
#include <maya/MTypeId.h>


class TimeInRanges : public MPxNode {
    public:
        TimeInRanges();
        ~TimeInRanges() override;
        MStatus compute(const MPlug & plug, MDataBlock & block) override;
        static void* creator();
        static MStatus initialize();
        static MTypeId id;
        static MObject disable;
        static MObject ranges;
        static MObject startFrame;
        static MObject endFrame;
        static MObject output;
        static MObject time;
};