import configparser
import os
import sys

# Get current paths:
config_file_name = 'configs.dat' # default name for the config file
config_sample_file_name = 'configs_sample.dat' # default name for the sample config file
cur_path = os.path.dirname(os.path.realpath(__file__)) # current path of this configs.py file
config_path = os.path.join(cur_path, config_file_name) # combined current path with config file name
config_sample_path = os.path.join(cur_path,config_sample_file_name) # combined current path with sample config file name
config_to_use = None # full path of the config file we're using

# Check if config file exists:
if not (os.path.exists(config_path)):
    # No config found at all. Looks for 'sample' one and warn user:
    print('No "configs.dat" file found.')
    if (os.path.exists(config_sample_path)):
        print('Found "configs_sample.dat". Please rename this to "configs.dat" for proper use')
        config_to_use = config_sample_path # assign sample dat to work as config
    else:
        raise Exception('No "config.dat" nor "config_sample.dat" found!')
        sys.exit()
else:
    config_to_use = config_path # config found. assign it for use.

# ConfigParser object
cp_obj = configparser.ConfigParser()

# Read the config file
def ReadConfigs():
    cp_obj.read(config_to_use)

# Save config file from current memory
def SaveConfigs():
    with open(config_to_use,'w') as _file:
        cp_obj.write(_file)

# Remove section if it exists
def RemoveSection(section):
    ReadConfigs()
    if (cp_obj.has_section(section)):
        cp_obj.remove_section(section)
        SaveConfigs()
    else:
        raise Exception('Section "%s" was not found!')

# Add section if it doesn't exists yet
def AddSection(new_section):
    ReadConfigs()
    if not (cp_obj.has_section(new_section)):
        cp_obj.add_section(new_section)
        SaveConfigs()
    else:
        raise Exception('Section "%s" already exists!' %new_section)

# Set new value for key, if section exists
def SetValue(section,key,new_value):
    ReadConfigs()
    if (cp_obj.has_section(section)):
        cp_obj.set(section, key, new_value)
        SaveConfigs()
    else:
        raise Exception('Section "%s" was not found!' % section)

# Get value if section/key exists
def GetValue(section,key):
    ReadConfigs()
    if (cp_obj.has_option(section,key)):
        return cp_obj.get(section, key)
    else:
        raise Exception("No section/key found")

def GetAllSections():
    ReadConfigs()
    return cp_obj.sections()

def GetNextSectionID():
    ReadConfigs()
    _all = [int(x) for x in GetAllSections()]
    for i in range(1,max(_all)+2):
        if (i not in _all):
            return i


# Read the configs during loading:
ReadConfigs()
