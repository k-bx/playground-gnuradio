"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, vectorSize=16):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Max Hold Block',   # will show up in GRC
            in_sig=[(np.float32, vectorSize), (np.float32, vectorSize)],
            out_sig=[(np.float32, vectorSize), (np.float32, vectorSize)],
        )
        


    def work(self, input_items, output_items):
        """example: multiply with constant"""
        for portIndex in range(len(input_items)):
            for vectorIndex in range(len(input_items[portIndex])):
                maxValue = np.max(input_items[portIndex][vectorIndex])
                for sampleIndex in range(len(input_items[portIndex][vectorIndex])):
                    output_items[portIndex][vectorIndex][sampleIndex] = maxValue
        return len(output_items[0])

