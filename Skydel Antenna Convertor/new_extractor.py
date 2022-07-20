"""
.ant file data extractor class for Antenna Pattern Convertor application.

Created on 31 03 20211

:author: Grace Oulai
:copyright: Skydel © 2021
:Version: 21.3.2
"""

import numpy as np
import pandas as pd


class NewAntReader:

    def __init__(self):
        pass

    @staticmethod
    def check_multi(fileName, lineSkip):
        header_info = pd.read_csv(fileName, error_bad_lines=False, delim_whitespace=None, nrows=3)
        freq1 = np.asarray(header_info.iloc[0, :], dtype=np.str)
        freq1, = np.char.split(freq1)
        freq1 = freq1[1]

        theta_sample = np.asarray(header_info.iloc[1, :], dtype=np.str)
        theta_sample, = np.char.split(theta_sample)
        theta_sample = theta_sample[4]

        phi_sample = np.asarray(header_info.iloc[2, :], dtype=np.str)
        phi_sample, = np.char.split(phi_sample)
        phi_sample = phi_sample[4]

        data = pd.read_csv(fileName, on_bad_lines='skip', delim_whitespace=True, skiprows=lineSkip - 1)
        occurrences = np.count_nonzero(data == '#Frequency:')
        return occurrences, data, freq1, theta_sample, phi_sample

    @staticmethod
    def read_info(data):

        freq = np.asarray(data.iloc[0, :])
        freq = freq[2]

        theta = np.array(data.iloc[:, 0], dtype=np.float64,
                         order='C')
        phi = np.asarray(data.iloc[:, 1], dtype=np.float64,
                         order='C')
        gain_total = np.asarray(data.iloc[:, 8], dtype=np.float64,
                                order='C')

        return freq, theta, phi, gain_total

    @staticmethod
    def slice_data(data, lineSkip):
        # "Occurrence greater than 1"
        result_array = np.where(data == '#Frequency:')
        result_array = result_array[0]
        debut = 0
        list_frequency = []
        list_data = []
        for array in result_array:
            freq = np.asarray(data.iloc[int(array), :])
            list_frequency.append(freq)
            new_data = data.iloc[debut:int(array)]
            list_data.append(new_data)
            debut = array + lineSkip - 1
        last_data = data.iloc[debut:len(data) - 1]
        list_data.append(last_data)

        return list_frequency, list_data

    @staticmethod
    def read_col(fileName, lineSkip):

        theta = np.empty(1000, dtype=object)
        phi = np.empty(1000, dtype=object)
        gain_total = np.empty(1000, dtype=object)
        line_skip = np.empty(1000, dtype=object)

        data = pd.read_csv(fileName, on_bad_lines="skip", delim_whitespace=True, skiprows=lineSkip - 1, header=None)
        occurrences = np.count_nonzero(data == '#Frequency:')
        if occurrences == 1:
            theta = np.array(data.iloc[:, 0], dtype=np.float64,
                             order='C')
            phi = np.asarray(data.iloc[:, 1], dtype=np.float64,
                             order='C')
            gain_total = np.asarray(data.iloc[:, 8], dtype=np.float64,
                                    order='C')
            line_skip = len(gain_total)

        else:
            result_array, array2 = np.where(data == '#Frequency:')
            debut = 0
            for array in result_array:
                new_data = data.iloc[debut:int(array)]
                list_frequency = np.asarray(data.iloc[int(array), :])
                debut = array

        return theta, phi, gain_total, line_skip

    @staticmethod
    def read_sample(fileName):
        with open(fileName, 'r') as f:
            lines = f.readlines()
            theta_sample = lines[2]
            theta_sample = theta_sample.split(': ')
            theta_sample = theta_sample[1]

            phi_sample = lines[3]
            phi_sample = phi_sample.split(': ')
            phi_sample = phi_sample[1]

        return theta_sample, phi_sample
