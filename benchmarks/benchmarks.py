# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.
import os
from shutil import rmtree

import numpy as np
import z5py
import z5py.util


class TimeSuite:
    """
    An example benchmark that times the performance of various kinds
    of iterating over dictionaries in Python.
    """
    tmp_folder = './tmp'
    file_read = './tmp/file_read.n5'
    file_write = './tmp/file_write.n5'

    def setup(self):
        self.data = z5py.util.fetch_test_data_stent()
        self.chunks = (64,) * 3
        try:
            os.mkdir(self.tmp_folder)
        except OSError:
            pass
        with z5py.File(self.file_read) as f:
            f.create_dataset('data_gzip', data=self.data,
                             compression='gzip', chunks=self.chunks)
            f.create_dataset('data_raw', data=self.data,
                             compression='raw', chunks=self.chunks)

    def teardown(self):
        try:
            rmtree(self.tmp_folder)
        except OSError:
            pass

    def time_write_raw(self):
        with z5py.File(self.file_write) as f:
            f.create_dataset('data_raw', data=self.data,
                             compression='raw', chunks=self.chunks)

    def time_write_gzip(self):
        with z5py.File(self.file_write) as f:
            f.create_dataset('data_gzip', data=self.data,
                             compression='gzip', chunks=self.chunks)

    def time_read_gzip(self):
        with z5py.File(self.file_read) as f:
            data = f['data_gzip'][:]

    def time_read_raw(self):
        with z5py.File(self.file_read) as f:
            data = f['data_raw'][:]


# class MemSuite:
#     def mem_list(self):
#         return [0] * 256
