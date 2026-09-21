"""
WSGI entry point for Apache mod_wsgi deployment.
This file is referenced in the Apache virtual host configuration
to serve the Flask application behind Apache.

See INSTALL.md for full Apache deployment instructions.
"""

import sys
import os

# Add the application directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app
from database import init_db

# Initialize the database on WSGI startup
init_db()

# The WSGI application object that Apache mod_wsgi will use
application = app
