# -*- coding: utf-8 -*-
import configparser
import os

# default name for the config file
config_file_name = 'configs.dat'
# default name for the sample config file
config_sample_file_name = 'configs_sample.dat'
# current path of configs.py file
cur_path = os.path.dirname(os.path.realpath(__file__))
# combined current path with config file name
config_path = os.path.join(cur_path, config_file_name)
# combined current path with sample config file name
config_sample_path = os.path.join(cur_path, config_sample_file_name)

# Check if config file exists:
if not (os.path.exists(config_path)):
    # No config found at all. Looks for 'sample' one and warn user:
    print('No "%s" file found.' % config_file_name)
    if os.path.exists(config_sample_path):
        print('Found "%s". Renaming this to "%s" for proper use.' %
              (config_sample_file_name, config_sample_path))
        os.rename(config_sample_path, config_path)
    else:
        print('No "%s" nor "%s" found!' %
              (config_file_name, config_sample_file_name))
        with open(config_file_name, 'w') as _file:
            _file.write('')
        print('Created default config file: %s.' % config_file_name)

# ConfigParser object
cp_obj = configparser.ConfigParser()


def ReadConfigs():
    """Read the config file"""
    cp_obj.read(config_path)


def SaveConfigs():
    """Save config file from current memory"""
    with open(config_path, 'w') as _File:
        cp_obj.write(_File)


def RemoveSection(section):
    """Remove section if it exists"""
    ReadConfigs()
    if cp_obj.has_section(section):
        cp_obj.remove_section(section)
        SaveConfigs()
    else:
        raise Exception('Section "%s" was not found!' % section)


def AddSection(new_section):
    """Add section if it doesn't exist yet"""
    ReadConfigs()
    if not (cp_obj.has_section(new_section)):
        cp_obj.add_section(new_section)
        SetValue(new_section, "Name", "")
        SetValue(new_section, "url", "http://")
        SetValue(new_section, "destination_folder", ".")
        SetValue(new_section, "last_download_time", '2089/01/01 23:59:59')
        SetValue(new_section, "next_download_time", '2090/01/01 23:59:59')
        SetValue(new_section, "download_type", "hour")
        SetValue(new_section, "frequency", "08:00:00")
        SetValue(new_section, "monday", 'True')
        SetValue(new_section, "tuesday", 'False')
        SetValue(new_section, "wednesday", 'False')
        SetValue(new_section, "thursday", 'False')
        SetValue(new_section, "friday", 'False')
        SetValue(new_section, "saturday", 'False')
        SetValue(new_section, "sunday", 'False')
        SetValue(new_section, "enabled", 'True')
        SaveConfigs()
    else:
        raise Exception('Section "%s" already exists!' % new_section)


def SetValue(section, key, new_value):
    """Set new value for key, if section exists"""
    ReadConfigs()
    if cp_obj.has_section(section):
        cp_obj.set(section, key, new_value)
        SaveConfigs()
    else:
        raise Exception('Section "%s" was not found!' % section)


def GetValue(section, key):
    """Get value if section & key exists"""
    ReadConfigs()
    if cp_obj.has_option(section, key):
        return cp_obj.get(section, key)
    else:
        raise Exception("No section/key found!")


# not used yet:
def GetBoolValue(section, key):
    # print('----------')
    # print('Section: %s' % section)
    # print('Key: %s' % key)
    """Get bool value if section & key exists"""
    ReadConfigs()
    if cp_obj.has_option(section, key):
        return cp_obj.getboolean(section, key)
    else:
        raise Exception("No section/key found!")


def GetAllSections():
    ReadConfigs()
    return cp_obj.sections()


def GetNextSectionID():
    """Returns next section ID, if there are gaps, will return that.
        if no gaps, will return next incremental ID"""
    ReadConfigs()
    # set all section names as integers, since we use them as IDs
    _all = [int(x) for x in GetAllSections()]
    # check if any sections exists at all
    if len(GetAllSections()) > 0:
        # check from 1 to n and assign next not-used ID,
        # where n is max ID used + 1
        for i in range(1, max(_all) + 2):
            if i not in _all:
                return str(i)


# Read the configs during loading:
ReadConfigs()
