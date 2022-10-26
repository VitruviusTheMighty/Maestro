import argparse
import enum
import logging

# import pyqtgraph as pg
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, LogLevels
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations, DetrendOperations
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams
# from pyqtgraph.Qt import QtGui, QtCore
import time
import numpy as np

def main():
    BoardShim.enable_dev_board_logger()
    DataFilter.enable_data_logger()
    MLModel.enable_ml_logger()
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=False, default=BoardIds.SYNTHETIC_BOARD)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    parser.add_argument('--master-board', type=int, help='master board id for streaming and playback boards',
                        required=False, default=BoardIds.NO_BOARD)
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.timeout = 0
    params.ip_port = 0
    params.ip_protocol = 0
    params.ip_address = ''
    params.serial_port = ''
    params.mac_address = ''
    params.other_info = ''
    params.serial_number = ''
    params.file = ''
    params.master_board = BoardIds.NO_BOARD # Only useful if we are streaming in

    try:
        board_shim = BoardShim(38, params)
        board_shim.prepare_session()
        board_shim.start_stream(450000, '')
        master_board_id = board_shim.get_board_id()
        BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
        time.sleep(1)
        # Graph(board_shim)
        # prep ML model
        sampling_rate = BoardShim.get_sampling_rate(master_board_id)
        nfft = DataFilter.get_nearest_power_of_two(sampling_rate)

        data = board_shim.get_board_data()
        

        eeg_channels = BoardShim.get_eeg_channels(int(master_board_id))
        bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate, True)
        feature_vector = bands[0]
        mindfulness_params = BrainFlowModelParams(BrainFlowMetrics.MINDFULNESS.value,
                                              BrainFlowClassifiers.DEFAULT_CLASSIFIER.value)
        mindfulness = MLModel(mindfulness_params)
        mindfulness.prepare()
        time.sleep(3)
        print('Mindfulness: %s' % str(mindfulness.predict(feature_vector)))

        while True:
            data = board_shim.get_current_board_data(sampling_rate)
            bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate, True)


            feature_vector = bands[0]
            alphas = []
            betas = []

            for channelIDX in range(len(BoardShim.get_exg_channels(38))):
                # DataFilter.detrend(data[channelIDX], DetrendOperations.LINEAR.value)
                psd = DataFilter.get_psd_welch(data[channelIDX], nfft, nfft // 2, sampling_rate,
                                   WindowOperations.BLACKMAN_HARRIS.value)
                alphas.append(DataFilter.get_band_power(psd, 7.0, 13.0))
                betas.append(DataFilter.get_band_power(psd, 14.0, 20.0))


            alpha = np.mean(alphas)
            beta = np.mean(betas)
            # print(np.array(bands).shape)
            print(f'A:{alpha}, B:{beta} :::Mindfulness: {str(mindfulness.predict(feature_vector))}' )
            time.sleep(1)
        mindfulness.release()




    except BaseException:
        logging.warning('Exception', exc_info=True)
    finally:
        if board_shim.is_prepared():
            logging.info('Releasing session')
            board_shim.release_session()


if __name__ == '__main__':
    main()