"""
Auto-generated Python code
Scenario : Data Storage
Prompt   : response_003.txt
Run      : 3
"""

import os
import pickle
import datetime
from datetime import timedelta
from pytz import timezone
import logging

# Set up logging
logging.basicConfig(filename='data_storage.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a class for data storage
class DataStorage:
    def __init__(self, data_dir='data', retention_period=30, timezone='US/Eastern'):
        self.data_dir = data_dir
        self.retention_period = retention_period  # days
        self.timezone = timezone

        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def _get_storage_file(self, data_id):
        # Get the storage file based on data ID and retention period
        file_name = f'{data_id}_{self.retention_period}d.pkl'
        return os.path.join(self.data_dir, file_name)

    def store_data(self, data_id, data):
        try:
            # Store data in a file with a timestamp
            file_path = self._get_storage_file(data_id)
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            logging.info(f'Data stored successfully for ID: {data_id}')
        except Exception as e:
            logging.error(f'Error storing data for ID: {data_id} - {e}')

    def retrieve_data(self, data_id):
        try:
            # Retrieve data from file based on data ID
            file_path = self._get_storage_file(data_id)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    data = pickle.load(f)
                    logging.info(f'Data retrieved successfully for ID: {data_id}')
                    return data
            else:
                logging.info(f'No data found for ID: {data_id}')
                return None
        except Exception as e:
            logging.error(f'Error retrieving data for ID: {data_id} - {e}')
            return None

    def purge_data(self):
        try:
            # Purge data older than retention period
            now = datetime.datetime.now(timezone(self.timezone))
            cutoff_date = now - timedelta(days=self.retention_period)
            for filename in os.listdir(self.data_dir):
                file_path = os.path.join(self.data_dir, filename)
                if os.path.isfile(file_path):
                    file_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_modified_time < cutoff_date:
                        os.remove(file_path)
                        logging.info(f'Data purged successfully for file: {filename}')
            logging.info('Data purge completed')
        except Exception as e:
            logging.error(f'Error purging data - {e}')

# Usage example
storage = DataStorage()

# Store data
storage.store_data('data1', {'key': 'value'})
storage.store_data('data2', {'key': 'value'})

# Retrieve data
data = storage.retrieve_data('data1')
print(data)

# Purge data
storage.purge_data()