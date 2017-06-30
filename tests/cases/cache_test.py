#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright 2014 Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

from .. import base

from girder.constants import SettingKey
from girder.utility import config
from girder.utility.model_importer import ModelImporter

import mock


def setUpModule():
    # Use memory caches for the test
    cfg = config.getConfig()
    cfg['cache']['enabled'] = True
    base.startServer()


def tearDownModule():
    base.stopServer()


class CacheTestCase(base.TestCase):
    def setUp(self):
        base.TestCase.setUp(self)

    def testCacheConfigurations(self):
        from girder.utility.cache import cache, requestCache

        self.assertTrue(cache.is_configured)
        self.assertTrue(requestCache.is_configured)

    def testSettingsCache(self):
        settingModel = ModelImporter.model('setting')

        settingModel.set(SettingKey.BRAND_NAME, 'foo')

        # change the brand name by sidestepping the cache
        setting = settingModel.findOne({'key': SettingKey.BRAND_NAME})
        setting['value'] = 'bar'

        # verify the cache still gives us the old brand name
        self.assertEquals(settingModel.get(SettingKey.BRAND_NAME), 'foo')

        # change the brand name through .set (which updates the cache)
        settingModel.set(SettingKey.BRAND_NAME, 'bar')

        # verify retrieving gives us the new one
        with mock.patch.object(settingModel, 'findOne') as findOneMock:
            self.assertEquals(settingModel.get(SettingKey.BRAND_NAME), 'bar')

            # findOne shouldn't be called since the cache is returning the setting
            findOneMock.assert_not_called()

        # unset the setting, invalidating the cache
        settingModel.unset(SettingKey.BRAND_NAME)

        # verify the database needs to be accessed to retrieve the setting now
        with mock.patch.object(settingModel, 'findOne') as findOneMock:
            settingModel.get(SettingKey.BRAND_NAME)

            findOneMock.assert_called_once()
