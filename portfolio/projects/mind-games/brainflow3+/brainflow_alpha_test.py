import argparse
import time
import brainflow
import numpy as np

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations


def main ():
    BoardShim.enable_dev_board_logger ()

    # use synthetic board for demo
    params = BrainFlowInputParams ()
    board_id = BoardIds.MUSE_2_BOARD.value
    sampling_rate = BoardShim.get_sampling_rate (board_id)
    board = BoardShim (board_id, params)
    board.prepare_session ()
    board.start_stream ()
    BoardShim.log_message (LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep (30)
    nfft = DataFilter.get_nearest_power_of_two (sampling_rate)
    data = board.get_board_data ()
    board.stop_stream ()
    board.release_session ()

    eeg_channels = BoardShim.get_eeg_channels (board_id)
    # second eeg channel of synthetic board is a sine wave at 10Hz, should see huge alpha
    eeg_channel = eeg_channels[1]
    # optional detrend
    DataFilter.detrend (data[eeg_channel], DetrendOperations.LINEAR.value)
    psd = DataFilter.get_psd_welch (data[eeg_channel], nfft, nfft // 2, sampling_rate, WindowFunctions.BLACKMAN_HARRIS.value)
    
    band_power_alpha = DataFilter.get_band_power (psd, 7.0, 13.0)
    band_power_beta = DataFilter.get_band_power (psd, 14.0, 20.0)
    print (f"alpha: {band_power_alpha}, beta: {band_power_beta}, alpha/beta:%f", band_power_alpha / band_power_beta)

    # fail test if ratio is not smth we expect
    # if (band_power_alpha / band_power_beta < 100):
    #     raise ValueError ('Wrong Ratio')


if __name__ == "__main__":
    main ()