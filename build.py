import os
import shutil
import sys


CURRENT_DIR = sys.path[0]
DEPENDENCIES_PATH = os.path.join(CURRENT_DIR, '.venv', 'Lib', 'site-packages')
BUILD_DIR = os.path.join(sys.path[0], 'dist')

print('Building app...')

# Delete dist dir
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)

# Create EXE
os.system(
    f'pyinstaller --noconsole --paths {DEPENDENCIES_PATH} --name cehub --onefile main.py'
)

# Create dirs
os.mkdir(os.path.join(BUILD_DIR, 'resources'))
os.mkdir(os.path.join(BUILD_DIR, 'data'))
os.mkdir(os.path.join(BUILD_DIR, 'instances'))

# Copy dir and files
shutil.copytree(
    os.path.join(CURRENT_DIR, 'resources', 'icons'),
    os.path.join(BUILD_DIR, 'resources', 'icons'),
)
shutil.copytree(
    os.path.join(CURRENT_DIR, 'resources', 'images'),
    os.path.join(BUILD_DIR, 'resources', 'images'),
)
shutil.copyfile(
    os.path.join(CURRENT_DIR, 'resources', 'resources.qrc'),
    os.path.join(BUILD_DIR, 'resources', 'resources.qrc'),
)
shutil.copytree(
    os.path.join(CURRENT_DIR, 'game'),
    os.path.join(BUILD_DIR, 'game'),
)
shutil.copyfile(
    os.path.join(CURRENT_DIR, 'data', 'data_initial.dat'),
    os.path.join(BUILD_DIR, 'data', 'data.dat'),
)

# Make zip
shutil.make_archive('cehub', 'zip', BUILD_DIR)
shutil.move(os.path.join(CURRENT_DIR, 'cehub.zip'), BUILD_DIR)

print('Build successfully!')
