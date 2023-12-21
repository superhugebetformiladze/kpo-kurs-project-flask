import unittest
from flask import url_for
from flask_testing import TestCase

import sys
import os
current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(root_directory)

from app import app

class MainSiteTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_index_page_status_code(self):
        response = self.client.get(url_for('client.index'))
        self.assertEqual(response.status_code, 200)

    def test_services_page_status_code(self):
        response = self.client.get(url_for('client.services'))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()