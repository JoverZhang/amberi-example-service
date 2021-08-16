from resource_management import *
from resource_management.libraries.script.script import Script

# Base configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
env = config['configurations']['example-env']

# Custom configurations
download_location = env['download_location']
install_directory = env['install_directory']
java_home = env['java_home']
