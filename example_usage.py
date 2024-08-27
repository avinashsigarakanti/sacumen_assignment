# Usage
# Reading Configurations

from source_code.config_source_code import ConfigurationHandler

handler = ConfigurationHandler()
handler.read_config('config.yaml')

# Writing to .env
handler.write_to_env_file('config.env')

# Writing to JSON
handler.write_to_json('config.json')

# Setting Environment Variables
handler.write_to_env()

# get the flat json
extracted_json = handler.get_config_as_json()
print(extracted_json)
