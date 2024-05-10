import os
import re
import logging
import pdb
from datetime import datetime

filename = f'puppet-fact-updates-{datetime.now()}.log'
logging.basicConfig(filename=filename, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

'''
    Actions:
        puppet_linter is called with a root_directory variable;
        traverse_directories is called, and iterates through folders and files recursviley and calls the replace_deprecated_facts function;
        replace_deprecated_facts will read a file, iterate through a dictionary and search for a set list of strings, if found, it will replace'
    
'''

# TODO Fix bugs, and check memory_size logic
# Includes top level sys

class puppet_linter:
    
    def __init__(self, root_directory, test=True):
        self.root_directory = root_directory
        self.replacements = { # Dictionary containing deprecated facts with their replacement counter-parts
            '$::architecture': "$facts['os']['architecture']",
            '$::augeasversion': "$facts['augeas']['version']",
            '$::bios_release_date': "$facts['dmi']['bios']['release_date']",
            '$::bios_vendor': "$facts['dmi']['bios']['vendor']",
            '$::bios_version': "$facts['dmi']['bios']['version']",
            '$::boardassettag': "$facts['dmi']['board']['asset_tag']",
            '$::boardmanufacturer': "$facts['dmi']['board']['manufacturer']",
            '$::boardproductname': "$facts['dmi']['board']['product']",
            '$::boardserialnumber': "$facts['dmi']['board']['serial_number']",
            '$::chassisassettag': "$facts['dmi']['chassis']['asset_tag']",
            '$::chassistype': "$facts['dmi']['chassis']['type']",
            '$::domain': "$facts['networking']['domain']",
            '$::fqdn': "$facts['networking']['fqdn']",
            '$::gid': "$facts['identity']['group']",
            '$::hardwareisa': "$facts['processors']['isa']",
            '$::hardwaremodel': "$facts['os']['hardware']",
            '$::hostname': "$facts['networking']['hostname']",
            '$::id': "$facts['identity']['user']",
            '$::ipaddress': "$facts['networking']['ip']",
            '$::ipaddress6': "$facts['networking']['ip6']",
            '$::lsbdistcodename': "$facts['os']['distro']['codename']",
            '$::lsbdistdescription': "$facts['os']['distro']['description']",
            '$::lsbdistid': "$facts['os']['distro']['id']",
            '$::lsbdistrelease': "$facts['os']['distro']['release']['full']",
            '$::lsbmajdistrelease': "$facts['os']['distro']['release']['major']",
            '$::lsbminordistrelease': "$facts['os']['distro']['release']['minor']",
            '$::lsbrelease': "$facts['os']['distro']['release']['specification']",
            '$::macaddress': "$facts['networking']['mac']",
            '$::macosx_buildversion': "$facts['os']['macosx']['build']",
            '$::macosx_productname': "$facts['os']['macosx']['product']",
            '$::macosx_productversion': "$facts['os']['macosx']['version']['full']",
            '$::macosx_productversion_major': "$facts['os']['macosx']['version']['major']",
            '$::macosx_productversion_minor': "$facts['os']['macosx']['version']['minor']",
            '$::manufacturer': "$facts['dmi']['manufacturer']",
            '$::memoryfree': "$facts['memory']['system']['available']",
            '$::memorysize': "$facts['memory']['system']['total']",
            '$::netmask': "$facts['networking']['netmask']",
            '$::netmask6': "$facts['networking']['netmask6']",
            '$::network': "$facts['networking']['network']",
            '$::network6': "$facts['networking']['network6']",
            '$::operatingsystem': "$facts['os']['name']",
            '$::operatingsystemmajrelease': "$facts['os']['release']['major']",
            '$::operatingsystemrelease': "$facts['os']['release']['full']",
            '$::osfamily': "$facts['os']['family']",
            '$::physicalprocessorcount': "$facts['processors']['physicalcount']",
            '$::processorcount': "$facts['processors']['count']",
            '$::productname': "$facts['dmi']['product']['name']",
            '$::rubyplatform': "$facts['ruby']['platform']",
            '$::rubysitedir': "$facts['ruby']['sitedir']",
            '$::rubyversion': "$facts['ruby']['version']",
            '$::selinux': "$facts['os']['selinux']['enabled']",
            '$::selinux_config_mode': "$facts['os']['selinux']['config_mode']",
            '$::selinux_config_policy': "$facts['os']['selinux']['config_policy']",
            '$::selinux_current_mode': "$facts['os']['selinux']['current_mode']",
            '$::selinux_enforced': "$facts['os']['selinux']['enforced']",
            '$::selinux_policyversion': "$facts['os']['selinux']['policy_version']",
            '$::serialnumber': "$facts['dmi']['product']['serial_number']",
            '$::swapencrypted': "$facts['memory']['swap']['encrypted']",
            '$::swapfree': "$facts['memory']['swap']['available']",
            '$::swapsize': "$facts['memory']['swap']['total']",
            '$::system32': "$facts['os']['windows']['system32']",
            '$::uptime': "$facts['system_uptime']['uptime']",
            '$::uptime_days': "$facts['system_uptime']['days']",
            '$::uptime_hours': "$facts['system_uptime']['hours']",
            '$::uptime_seconds': "$facts['system_uptime']['seconds']",
            '$::uuid': "$facts['dmi']['product']['uuid']",
            '$::xendomains': "$facts['xen']['domains']",
            '$::zonename': "$facts['solaris_zones']['current']"
        } 
        self.test = test
        self.traverse_directories()
        
    def replace_deprecated_facts(self, file_path, is_erb=False):
        # Open file to read its contents
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Store the original content to compare later
        original_content = content

        # Uses Regex to find the deprecated variable usage and replace it
        # TODO Find regex for ERB templates, and old $factname syntax
        for deprecated, replacement in self.replacements.items(): # Iterates through replacement dictionary, searching for uses of Deprecated Facts
            
            search_strings = [deprecated, deprecated.replace('::', '')] # $::factname, $factname, @factname'
            
            if is_erb: # If file is .erb, look for ruby facter usage
                search_strings =['@' + deprecated.strip('$::')]
                
            for search_string in search_strings:  
                if search_string in original_content: #  Log if deprecated fact is found in original file
                    logging.info(f'{search_string} found in {file_path}')
                    if not self.test:
                        if is_erb is False:
                            content = re.sub(re.escape(search_string), replacement, content) # Replaces deprecated fact string, with replacement string
                        else:
                            content = re.sub(re.escape(search_string), replacement.replace('$', '@'), content) # Replaces deprecated fact, with @replacementfact
                        if search_string in content: # Log if deprecated fact that was found has been removed
                            logging.error(f'{search_string} has not been removed from {file_path}')       
                        else:
                            logging.info(f'{search_string} has been successfully removed from {file_path}')
                    else:
                        logging.info(f'TEST: {search_string} would have been removed from {file_path}')
                else:
                # VERBOSE logging.info(f'{search_string} was not found in {file_path}')
                    pass

        # Writes to file if there were any changes        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            logging.info(f"Updated {file_path} with replacement facts")
            
    # Recursively replaces deprecated facts
    def traverse_directories(self):
        for root, dirs, files in os.walk(self.root_directory):
            for file in files:
                if file.endswith('.pp'):
                    self.replace_deprecated_facts(os.path.join(root, file))
                elif file.endswith('.erb'):
                    self.replace_deprecated_facts(os.path.join(root, file), is_erb=True)


if __name__ == "__main__":
    #root_directory = '/Users/dmw532/dps-puppet-control-lms/modules'
    root_directory = '/Users/dmw532/automate/linter/test_dir'
    pl = puppet_linter(root_directory)
