#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: kb
# GNU Radio version: 3.10.2.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class SSB_rcv_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "SSB_rcv_test")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 256000
        self.audio_rate = audio_rate = 32000
        self.volume = volume = 0.2
        self.tuning = tuning = 51500
        self.reverse = reverse = 1
        self.decim = decim = int(samp_rate / audio_rate)
        self.carrier_freq = carrier_freq = 53000
        self.bfo = bfo = 1500

        ##################################################
        # Blocks
        ##################################################
        self._volume_range = Range(0, 1.0, 0.05, 0.2, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, "Volume", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._volume_win)
        self._tuning_range = Range(48000, 58000, 100, 51500, 200)
        self._tuning_win = RangeWidget(self._tuning_range, self.set_tuning, "Tuning", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tuning_win)
        # Create the options list
        self._reverse_options = [-1, 1]
        # Create the labels list
        self._reverse_labels = ['Upper', 'Lower']
        # Create the combo box
        self._reverse_tool_bar = Qt.QToolBar(self)
        self._reverse_tool_bar.addWidget(Qt.QLabel("Sideband" + ": "))
        self._reverse_combo_box = Qt.QComboBox()
        self._reverse_tool_bar.addWidget(self._reverse_combo_box)
        for _label in self._reverse_labels: self._reverse_combo_box.addItem(_label)
        self._reverse_callback = lambda i: Qt.QMetaObject.invokeMethod(self._reverse_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._reverse_options.index(i)))
        self._reverse_callback(self.reverse)
        self._reverse_combo_box.currentIndexChanged.connect(
            lambda i: self.set_reverse(self._reverse_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._reverse_tool_bar)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decim, firdes.low_pass(1.0, samp_rate, 3000, 100), tuning, samp_rate)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_ff(reverse)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(volume)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.000100)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/Users/kb/Nextcloud/Documents/GNURadio/ssb_lsb_256k_complex2.dat', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self._bfo_range = Range(0, 3000, 10, 1500, 200)
        self._bfo_win = RangeWidget(self._bfo_range, self.set_bfo, "Fine tuning", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._bfo_win)
        self.audio_sink_0 = audio.sink(32000, '', True)
        self.analog_sig_source_x_1 = analog.sig_source_f(audio_rate, analog.GR_SIN_WAVE, 1500, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(audio_rate, analog.GR_COS_WAVE, 1500, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_complex_to_float_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "SSB_rcv_test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_decim(int(self.samp_rate / self.audio_rate))
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1.0, self.samp_rate, 3000, 100))

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.set_decim(int(self.samp_rate / self.audio_rate))
        self.analog_sig_source_x_0.set_sampling_freq(self.audio_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.audio_rate)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_1.set_k(self.volume)

    def get_tuning(self):
        return self.tuning

    def set_tuning(self, tuning):
        self.tuning = tuning
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.tuning)

    def get_reverse(self):
        return self.reverse

    def set_reverse(self, reverse):
        self.reverse = reverse
        self._reverse_callback(self.reverse)
        self.blocks_multiply_const_vxx_2.set_k(self.reverse)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq

    def get_bfo(self):
        return self.bfo

    def set_bfo(self, bfo):
        self.bfo = bfo




def main(top_block_cls=SSB_rcv_test, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
