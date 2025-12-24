"""Test configuration to keep unit tests self contained."""

import os
import tempfile


# Use a throwaway SQLite database when running tests to avoid a Postgres dependency
os.environ.setdefault('DATABASE_URL', f"sqlite:///{tempfile.gettempdir()}/aura_test.db")
