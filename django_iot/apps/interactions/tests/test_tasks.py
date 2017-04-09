from django.test import TestCase
from django_iot.apps.interactions import tasks


# all tests should fail with NotImplementedError before implementing tasks


class TestPullAttributes(TestCase):
    def test_run(self):
        tasks.pull_attributes()


class TestPullStatus(TestCase):
    def test_run(self):
        tasks.pull_status()


class TestRefreshAll(TestCase):
    def test_run(self):
        tasks.refresh_all()


class TestSetStatus(TestCase):
    def test_run(self):
        tasks.set_status()


class TestSetAttributes(TestCase):
    def test_run(self):
        tasks.set_attributes()
