import pandas as pd
import pytest
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
from src.reports import spending_category, write_to_file


