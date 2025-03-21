from datetime import datetime, timedelta
import json
from decimal import Decimal

def get_dates_in_range(start_date: str, end_date: str, date_format: str = "%Y-%m-%d"):
    """
    Returns a list of dates between start_date and end_date (inclusive).
    
    :param start_date: Start date as a string (e.g., "2025-03-01")
    :param end_date: End date as a string (e.g., "2025-03-05")
    :param date_format: The format of the input dates (default is "%Y-%m-%d")
    :return: List of date strings in the same format.
    """
    # Convert string dates to datetime objects
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)

    # Generate dates in range (inclusive)
    date_list = [(start + timedelta(days=i)).strftime(date_format) for i in range((end - start).days + 1)]
    
    return date_list

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)
