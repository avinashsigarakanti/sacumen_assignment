import pytest
import os
import json
import yaml
import logging as logger
from source_code.config_source_code import ConfigurationHandler

@pytest.fixture
def setup_config_handler():
    """
    Fixture to create a new instance of ConfigurationHandler for each test.
    """
    logger.info("Creating a new instance of ConfigurationHandler")
    return ConfigurationHandler()

def test_read_yaml(setup_config_handler):
    """
    Test reading a YAML configuration file.
    """
    # Arrange: Create a temporary YAML file
    yaml_content = {'key': 'value'}
    yaml_file = 'test.yaml'
    logger.info(f"Creating temporary YAML file {yaml_file}")
    with open(yaml_file, 'w') as file:
        yaml.dump(yaml_content, file)

    # Act: Read the YAML file
    logger.info(f"Reading YAML file {yaml_file}")
    setup_config_handler.read_config(yaml_file)

    # Assert: Check if the config is correctly read
    assert setup_config_handler.config == yaml_content
    logger.info("YAML file read successfully")

    # Cleanup: Remove the test YAML file
    os.remove(yaml_file)
    logger.info(f"Removed temporary YAML file {yaml_file}")

def test_read_ini(setup_config_handler):
    """
    Test reading an INI configuration file.
    """
    # Arrange: Create a temporary INI file
    ini_content = '[section]\nkey = value\n'
    ini_file = 'test.cfg'
    logger.info(f"Creating temporary INI file {ini_file}")
    with open(ini_file, 'w') as file:
        file.write(ini_content)

    # Act: Read the INI file
    logger.info(f"Reading INI file {ini_file}")
    setup_config_handler.read_config(ini_file)

    # Assert: Check if the config is correctly read
    expected_config = {'section': {'key': 'value'}}
    assert setup_config_handler.config == expected_config
    logger.info("INI file read successfully")

    # Cleanup: Remove the test INI file
    os.remove(ini_file)
    logger.info(f"Removed temporary INI file {ini_file}")

def test_write_to_json(setup_config_handler):
    """
    Test writing the configuration dictionary to a JSON file.
    """
    # Arrange: Set a sample config
    config_content = {'key': 'value'}
    setup_config_handler.config = config_content
    json_file = 'test.json'
    logger.info(f"Preparing to write configuration to JSON file {json_file}")

    # Act: Write to a JSON file
    setup_config_handler.write_to_json(json_file)

    # Assert: Check if the JSON file contains the correct data
    logger.info(f"Reading JSON file {json_file}")
    with open(json_file) as file:
        data = json.load(file)
    assert data == config_content
    logger.info("JSON file written successfully")

    # Cleanup: Remove the test JSON file
    os.remove(json_file)
    logger.info(f"Removed temporary JSON file {json_file}")

def test_write_to_env(setup_config_handler):
    """
    Test writing the configuration dictionary to OS environment variables.
    """
    # Arrange: Set a sample config
    config_content = {'key': 'value'}
    setup_config_handler.config = config_content
    logger.info("Setting environment variables")

    # Act: Write to environment variables
    setup_config_handler.write_to_env()

    # Assert: Check if the environment variable is correctly set
    assert os.getenv('key') == 'value'
    logger.info("Environment variable set successfully")

    # Cleanup: Unset the environment variable
    del os.environ['key']
    logger.info("Environment variable unset")

def test_write_to_env_file(setup_config_handler):
    """
    Test writing the configuration dictionary to a .env file.
    """
    # Arrange: Set a sample config
    config_content = {'key': 'value'}
    setup_config_handler.config = config_content
    env_file = 'test.env'
    logger.info(f"Preparing to write configuration to .env file {env_file}")

    # Act: Write to a .env file
    setup_config_handler.write_to_env_file(env_file)

    # Assert: Check if the .env file contains the correct data
    logger.info(f"Reading .env file {env_file}")
    with open(env_file) as file:
        lines = file.readlines()
    expected_lines = ['key=value\n']
    assert lines == expected_lines
    logger.info(".env file written successfully")

    # Cleanup: Remove the test .env file
    os.remove(env_file)
    logger.info(f"Removed temporary .env file {env_file}")
