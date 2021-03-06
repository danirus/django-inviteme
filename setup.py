from setuptools import setup, find_packages
from setuptools.command.test import test

def run_tests(*args):
    from inviteme.tests import run_tests
    run_tests()

test.run_tests = run_tests

setup(
    name = "django-inviteme",
    version = "1.0a2",
    packages = find_packages(),
    license = "MIT",
    description = "Django invite-me form App with email verification",
    long_description = "A reusable Django app that adds an email address submission form with protection. Email addresses will only hit the database when users confirm them.",
    author = "Daniel Rus Morales",
    author_email = "inbox@danir.us",
    maintainer = "Daniel Rus Morales",
    maintainer_email = "inbox@danir.us",
    url = "http://github.com/danirus/django-inviteme/",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    test_suite = "dummy",
)
