import os
import re

replacements = {
    '$::fqdn': "$facts['networking']['fqdn']",
    '$::hostname': "$facts['networking']['hostname']",
    '$::ipaddress': "$facts['networking']['ip']",
    '$::lsbdistcodename': "$facts['os']['distro']['codename']",
    '$::lsbdistrelease': "$facts['os']['distro']['release']['full']",
    '$::lsbmajdistrelease': "$facts['os']['distro']['release']['major']",
    '$::memorysize_mb': "$facts['memory']['system']['total_bytes']",
    '$::operatingsystem': "$facts['os']['name']",
    '$::operatingsystemmajrelease': "$facts['os']['release']['major']",
    '$::operatingsystemrelease': "$facts['os']['release']['full']",
    '$::osfamily': "$facts['os']['family']",
    '$::processorcount': "$facts['processors']['count']"
}

def replace_deprecated_facts(file_path, replacements, is_erb=False):
    # Open file to read its contents
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Store the original content to compare later
    original_content = content

    # Regex to find the deprecated variable usage and replace it
    for deprecated, replacement in replacements.items():
        content = re.sub(re.escape(deprecated), replacement, content)

    # Prepare and perform the replacements
    for deprecated, replacement in replacements.items():
        # Adjust the pattern to match both scoped and unscoped variables
        pattern = r'\$(::)?' + re.escape(deprecated.lstrip('$'))
        if is_erb:
            # For ERB templates, regex pattern is different, and replacement/content is different
            pass
        
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    # Writes to file if there were any changes        
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {file_path}")
        
# Recursively replaces deprecated facts
def traverse_directories(root_directory):
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.pp'):
                replace_deprecated_facts(os.path.join(root, file), replacements)
            elif file.endswith('.erb'):
                replace_deprecated_facts(os.path.join(root, file), replacements, is_erb=True)


if __name__ == "__main__":
    #root_directory = '~/dps-puppet-control-lms'
    root_directory = './test_dir'
    traverse_directories(root_directory)