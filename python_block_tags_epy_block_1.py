"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Detection Counter',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.samplesSinceDetection = 0

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        tagTuple = self.get_tags_in_window(0, 0, len(input_items[0]))
        relativeOffsetList = []
        for tag in tagTuple:
            if pmt.to_python(tag.key) == 'detect':
                relativeOffsetList.append(tag.offset - self.nitems_read(0))
        relativeOffsetList.sort()
        for index in range(len(output_items[0])):
            output_items[0][index] = self.samplesSinceDetection
            if len(relativeOffsetList) > 0 and index >= relativeOffsetList[0]:
                relativeOffsetList.pop(0)
                self.samplesSinceDetection = 0
            else:
                self.samplesSinceDetection = self.samplesSinceDetection + 1
        return len(output_items[0])
