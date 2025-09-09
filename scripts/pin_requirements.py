#!/usr/bin/env python3
"""
Pin/unpin requirements.txt versions for security auditing.
"""

import argparse
import re
from pathlib import Path

def extract_version_from_requirement(requirement_line):
    """Extract the minimum version from a requirement line."""
    # Match patterns like package>=1.2.3 or package==1.2.3
    match = re.search(r'([a-zA-Z0-9_-]+)([><=!]+)([0-9.]+)', requirement_line)
    if match:
        package_name, operator, version = match.groups()
        return package_name, version
    return None, None

def unpin_requirements(filename='requirements.txt'):
    """Convert pinned requirements back to flexible versions."""
    requirements_file = Path.cwd() / filename
    
    print(f"Looking for requirements.txt at: {requirements_file.absolute()}")
    if not requirements_file.exists():
        print("requirements.txt not found!")
        return False
    
    # Read current requirements
    with open(requirements_file, 'r') as f:
        lines = f.readlines()
    
    print(f"Read {len(lines)} lines from requirements.txt")
    unpinned_lines = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            unpinned_lines.append(line)
            continue
            
        # Convert == to >=
        if '==' in line:
            unpinned_line = line.replace('==', '>=')
            unpinned_lines.append(unpinned_line)
            package_name = line.split('==')[0]
            print(f"Unpinned {package_name}")
        else:
            unpinned_lines.append(line)
    
    # Write unpinned requirements back to file
    with open(requirements_file, 'w') as f:
        for line in unpinned_lines:
            f.write(line + '\n')
    
    print(f"Updated {requirements_file} with flexible versions")
    return True

def pin_requirements(filename='requirements.txt'):
    """Convert flexible requirements to pinned versions in a temporary file."""
    requirements_file = Path.cwd() / filename
    base_name = Path(filename).stem
    pinned_file = Path.cwd() / f'{base_name}-pinned.txt'
    
    print(f"Looking for requirements.txt at: {requirements_file.absolute()}")
    if not requirements_file.exists():
        print("requirements.txt not found!")
        return False
    
    # Read current requirements
    with open(requirements_file, 'r') as f:
        lines = f.readlines()
    
    print(f"Read {len(lines)} lines from requirements.txt")
    pinned_lines = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            pinned_lines.append(line)
            continue
            
        # Extract package name and version from requirement
        package_name, version = extract_version_from_requirement(line)
        
        if package_name and version:
            pinned_lines.append(f"{package_name}=={version}")
            print(f"Pinned {package_name} to minimum version {version}")
        else:
            print(f"Warning: Could not parse requirement '{line}', keeping original")
            pinned_lines.append(line)
    
    # Write pinned requirements to temporary file
    with open(pinned_file, 'w') as f:
        for line in pinned_lines:
            f.write(line + '\n')
    
    print(f"Created {pinned_file} with pinned versions")
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Pin or unpin requirements file versions for security auditing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python pin_requirements.py pin
  python pin_requirements.py unpin
  python pin_requirements.py pin requirements-dev.txt
  python pin_requirements.py unpin my-requirements.txt"""
    )
    parser.add_argument('action', choices=['pin', 'unpin'], 
                       help='pin: convert >= to == using minimum versions; unpin: convert == to >=')
    parser.add_argument('filename', nargs='?', default='requirements.txt',
                       help='requirements file to process (default: requirements.txt)')
    args = parser.parse_args()
    
    if args.action == 'pin':
        if pin_requirements(args.filename):
            print("Requirements successfully pinned!")
        else:
            print("Failed to pin requirements")
            exit(1)
    elif args.action == 'unpin':
        if unpin_requirements(args.filename):
            print("Requirements successfully unpinned!")
        else:
            print("Failed to unpin requirements")
            exit(1)