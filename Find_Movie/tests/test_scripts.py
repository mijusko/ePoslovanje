import subprocess
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch


class ScriptExecutionTests(TestCase):
    @patch('subprocess.run')
    def test_run_torrent_script_success(self, mock_subprocess):
        mock_subprocess.return_value.stdout = 'Script output'
        response = self.client.get(
            reverse('run_torrent_script', args=['test_movie']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Script executed successfully',
                      response.json()['message'])
        self.assertEqual(response.json()['output'], 'Script output')

    @patch('subprocess.run')
    def test_run_torrent_script_failure(self, mock_subprocess):
        mock_subprocess.side_effect = subprocess.CalledProcessError(
            1, 'python')
        response = self.client.get(
            reverse('run_torrent_script', args=['test_movie']))
        self.assertEqual(response.status_code, 500)
        self.assertIn('Failed to execute script', response.json()['error'])

    @patch('subprocess.run')
    def test_run_subtitle_script_success(self, mock_subprocess):
        mock_subprocess.return_value.stdout = 'Subtitle output'
        response = self.client.get(
            reverse('run_subtitle_script', args=['test_movie']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Script executed successfully',
                      response.json()['message'])
        self.assertEqual(response.json()['output'], 'Subtitle output')

    @patch('subprocess.run')
    def test_run_subtitle_script_failure(self, mock_subprocess):
        mock_subprocess.side_effect = subprocess.CalledProcessError(
            1, 'python')
        response = self.client.get(
            reverse('run_subtitle_script', args=['test_movie']))
        self.assertEqual(response.status_code, 500)
        self.assertIn('Failed to execute script', response.json()['error'])
