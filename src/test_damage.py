#!/usr/bin/env python
from __future__ import print_function

__author__ = 'Hyeuk Ryu'

import unittest
import os
import filecmp
import pandas as pd

from core.damage import WindDamageSimulator
import core.database as database
import core.scenario as scenario


class options(object):

    def __init__(self):
        self.output_folder = None


class TestWindDamageSimulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        path = '/'.join(__file__.split('/')[:-1])
        cls.path_reference = os.path.join(path, 'test/output')
        cls.path_output = os.path.join(path, 'output')

        for the_file in os.listdir(cls.path_output):
            file_path = os.path.join(cls.path_output, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

        # model_db = os.path.join(path_, './core/output/model.db')
        # model_db = os.path.join(path_, '../data/model.db')
        model_db = os.path.join(path, 'model.db')
        database.configure(model_db)

        scenario1 = scenario.loadFromCSV(os.path.join(path,
                                                      'scenarios/carl1.cfg'))
        scenario1.flags['random_seed'] = True

        option = options()
        option.output_folder = cls.path_output

        cls.mySim = WindDamageSimulator(option, None, None)
        cls.mySim.set_scenario(scenario1)
        cls.mySim.simulator_mainloop()

    @classmethod
    def tearDownClass(cls):
        database.db.close()

        # delete test/output
        # os.path.join(path_, 'test/output')

    def test_random_seed(self):
        self.assertEqual(self.mySim.s.flags['random_seed'], True)

    def check_file_consistency(self, file1, file2, **kwargs):

        identical = filecmp.cmp(file1, file2)

        if not identical:
            try:
                data1 = pd.read_csv(file1, **kwargs)
                data2 = pd.read_csv(file2, **kwargs)

                pd.util.testing.assert_frame_equal(data1, data2)
            except AssertionError:
                print('{} and {} are different'.format(file1, file2))

    def test_consistency_house_cpi(self):
        filename = 'house_cpi.csv'
        file1 = os.path.join(self.path_reference, filename)
        file2 = os.path.join(self.path_output, filename)
        self.check_file_consistency(file1, file2)

    def test_consistency_house_damage(self):
        filename = 'house_damage.csv'
        file1 = os.path.join(self.path_reference, filename)
        file2 = os.path.join(self.path_output, filename)
        self.check_file_consistency(file1, file2)

    def test_consistency_house_damage_idx(self):
        filename = 'house_dmg_idx.csv'
        file1 = os.path.join(self.path_reference, filename)
        file2 = os.path.join(self.path_output, filename)
        self.check_file_consistency(file1, file2)

    def test_consistency_fragilites(self):
        filename = 'fragilities.csv'
        file1 = os.path.join(self.path_reference, filename)
        file2 = os.path.join(self.path_output, filename)
        self.check_file_consistency(file1, file2)

    def test_consistency_houses_damaged(self):
        filename = 'houses_damaged_at_v.csv'
        file1 = os.path.join(self.path_reference, filename)
        file2 = os.path.join(self.path_output, filename)
        self.check_file_consistency(file1, file2, skiprows=3)

    def test_consistency_wateringress(self):
        filename = 'wateringress.csv'
        file1 = os.path.join(self.path_reference, filename)
        file2 = os.path.join(self.path_output, filename)
        self.check_file_consistency(file1, file2)

    def test_consistency_wind_debris(self):
        filename = 'wind_debris.csv'
        file1 = os.path.join(self.path_reference, filename)
        file2 = os.path.join(self.path_output, filename)
        self.check_file_consistency(file1, file2)

if __name__ == '__main__':
    unittest.main()
