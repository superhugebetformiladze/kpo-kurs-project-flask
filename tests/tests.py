import unittest
from flask import url_for
from flask_testing import TestCase
from unittest.mock import patch, MagicMock

import sys
import os
current_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(root_directory)

from app import app
from utils.config_utils import get_telegram_config

telegram_config = get_telegram_config()
chat_id = telegram_config["chat_id"]

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
        
    def test_service_detail_page_status_code(self):
        response = self.client.get(url_for('client.service_detail', service_id=1))
        self.assertEqual(response.status_code, 200)

    def test_profile_page_status_code_logged_in(self):
        self.client.post(url_for('auth.login'), data=dict(
            login='admin',
            password='admin1234'
        ), follow_redirects=True)

        response = self.client.get(url_for('client.profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_page_status_code_not_logged_in(self):
        self.client.get(url_for('auth.logout'), follow_redirects=True)

        response = self.client.get(url_for('client.profile'))
        self.assertEqual(response.status_code, 401)

    def test_admin_home_page_status_code_logged_in(self):
        self.client.post(url_for('auth.login'), data=dict(
            login='admin',
            password='admin1234'
        ), follow_redirects=True)
        response = self.client.get(url_for('admin.admin_home'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_services_page_status_code_logged_in(self):
        self.client.post(url_for('auth.login'), data=dict(
            login='admin',
            password='admin1234'
        ), follow_redirects=True)
        response = self.client.get(url_for('admin.admin_services'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_create_service_page_status_code_logged_in(self):
        self.client.post(url_for('auth.login'), data=dict(
            login='admin',
            password='admin1234'
        ), follow_redirects=True)
        response = self.client.get(url_for('admin.admin_create_service'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_edit_service_page_status_code_logged_in(self):
        self.client.post(url_for('auth.login'), data=dict(
            login='admin',
            password='admin1234'
        ), follow_redirects=True)
        response = self.client.get(url_for('admin.admin_edit_service', service_id=1))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_users_page_status_code_logged_in(self):
        self.client.post(url_for('auth.login'), data=dict(
            login='admin',
            password='admin1234'
        ), follow_redirects=True)
        response = self.client.get(url_for('admin.admin_users'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_requests_page_status_code_logged_in(self):
        self.client.post(url_for('auth.login'), data=dict(
            login='admin',
            password='admin1234'
        ), follow_redirects=True)
        response = self.client.get(url_for('admin.admin_requests'))
        self.assertEqual(response.status_code, 200)


    @patch('website.client.routes.client_routes.Bot.send_message')
    def test_submit_request(self, mock_send_message):
        self.client.post(url_for('auth.login'), data=dict(
            login='admin',
            password='admin1234'
        ), follow_redirects=True)

        response = self.client.post(url_for('client.index'), data=dict(
            client_name='John Doe',
            car_brand='Toyota',
            car_model='Camry',
            service_name='Oil Change',
            phone_number='1234567890'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        mock_send_message.assert_called_once_with(chat_id, (
            "Новая заявка!\n\n"
            f"Имя: John Doe\n"
            f"Марка автомобиля: Toyota\n"
            f"Модель автомобиля: Camry\n"
            f"Услуга: Oil Change\n"
            f"Номер телефона: 1234567890"
        ))
    

if __name__ == '__main__':
    unittest.main()