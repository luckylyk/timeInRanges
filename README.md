# Time In Ranges

### Description
Plug-in for Autodesk Maya. Add a custom node to compute if a given time is in given time ranges.

### Installation
Add the folder which contains the *.mll/.so* plug in in the MAYA_PLUGIN_PATHS
Copy the *timeInRange.py* found in the scripts folder into the maya scripts folder.

### Usage
```python
from maya import cmds
cmds.loadPlugin("timeInRanges")

import time_in_ranges
# node can be any node having an lodVisibility attribute.
# shot is a shot node as string.
time_in_ranges.add_node_to_shot_range_visibility(node, shot)
time_in_ranges.remove_node_from_shot_range_visibility(node, shot)

# Enable/Disable all the nodes
time_in_ranges.set_time_in_ranges_enabled(True)
```