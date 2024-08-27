import os
import json
import yaml
from configparser import ConfigParser
import logging as logger

class ConfigurationHandler:
    """
    The class is defined to handle the to handle configuration files and its operations.

    This class can read the files with the format .yaml, .cfg, and .conf
    and also can write the configurations to .env files, .json files, or set them
    as OS environment variables.
    """
    def __init__(self):
        """
        Initializes the ConfigurationHandler with an empty configuration dictionary.
        """
        self.config = {}

    def read_config_file(self, file_path):
        """
        Reads the configuration from the specified file based on its extension.

        Args:
            file_path (str): The path to the configuration file.

        Raises:
            ValueError: If the file extension is not supported.
        """
        try:
            ext = file_path.split('.')[-1].lower()
            if ext == 'yaml':
                self.read_yaml_file(file_path)
            elif ext in ('cfg', 'conf'):
                self.read_ini(file_path)
            else:
                raise ValueError("Unsupported file format")
        except Exception as e:
            logger.error(f"Failed to read config file {file_path}: {e}")
            raise

    def read_yaml_file(self, file_path ):
        """
        Reads a YAML configuration file and updates the internal configuration dictionary.

        Args:
            file_path (str): The path to the YAML configuration file.

        Raises:
            FileNotFoundError: If the file does not exist.
            yaml.YAMLError: If there is an error parsing the YAML file.
        """
        try:
            with open(file_path, 'r') as file:
                self.config = yaml.safe_load(file) or {}
            logger.info(f"Successfully read YAML config file {file_path}")
        except FileNotFoundError:
            logger.error(f"YAML file not found: {file_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file {file_path}: {e}")
            raise

    def read_ini(self, file_path):
        """
        Reads an INI configuration file and updates the internal configuration dictionary.

        Args:
            file_path (str): The path to the INI configuration file.

        Raises:
            FileNotFoundError: If the file does not exist.
            configparser.Error: If there is an error reading the INI file.
        """
        try:
            parser = ConfigParser()
            parser.read(file_path)
            self.config = {section: dict(parser.items(section)) for section in parser.sections()}
            logger.info(f"Successfully read INI config file {file_path}")
        except FileNotFoundError:
            logger.error(f"INI file not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error reading INI file {file_path}: {e}")
            raise

    def write_to_env(self):
        """
        Writes the current configuration dictionary to the OS environment variables.

        Raises:
            Exception: If an error occurs while setting environment variables.
        """
        try:
            for key, value in self.config.items():
                os.environ[key] = str(value)
            logger.info("Successfully written configuration to environment variables")
        except Exception as e:
            logger.error(f"Failed to write configuration to environment variables: {e}")
            raise

    def write_to_json(self, file_path):
        """
        Writes the current configuration dictionary to a JSON file.

        Args:
            file_path (str): The path to the JSON file.

        Raises:
            IOError: If there is an error writing to the file.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(self.config, file, indent=4)
            logger.info(f"Successfully written configuration to JSON file {file_path}")
        except IOError as e:
            logger.error(f"Failed to write JSON file {file_path}: {e}")
            raise

    def write_to_env_file(self, file_path):
        """
        Write the flattened configuration to a .env file.

        Args:
            file_path (str): The path to the .env file.

        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(file_path , 'w') as file:
                flattened_config = self.flatten_dict(self.config)
                for key , value in flattened_config.items():
                    file.write(f"{key}={value}\n")
                logger.info(f"Successfully wrote configuration to .env file: {file_path}")
        except IOError as e:
            logger.error(f"Error writing to .env file: {e}")
            raise

    def flatten_dict(self, d, parent_key='', sep='_'):
        """
        Flatten a nested dictionary into a single-level dictionary with dot-separated keys.

        Args:
            d (dict): The dictionary to flatten.
            parent_key (str, optional): The base key to prepend to each key in the dictionary. Defaults to ''.
            sep (str, optional): Separator to use between parent and child keys. Defaults to '_'.

        Returns:
            dict: A flat dictionary with dot-separated keys.

        Raises:
            TypeError: If the input is not a dictionary.
        """
        if not isinstance(d , dict) :
            raise TypeError("Input must be a dictionary")

        items = []
        for k , v in d.items() :
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v , dict) :
                items.extend(self.flatten_dict(v , new_key , sep=sep).items())
            else :
                items.append((new_key , v))
        return dict(items)

    def get_config_as_json(self):
        """
        Returns the configuration as a JSON-formatted string.

        Returns:
            str: The configuration in JSON format.

        Raises:
            TypeError: If the configuration is not a dictionary.
        """
        try:
            if not isinstance(self.config , dict):
                raise TypeError("Configuration must be a dictionary")
            json_config = json.dumps(self.config , indent=4)
            logger.info("Successfully converted configuration to JSON")
            return json_config
        except Exception as e:
            logger.error(f"Error converting configuration to JSON: {e}")
            raise