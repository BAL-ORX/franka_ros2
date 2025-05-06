from setuptools import find_packages, setup
import os                       #  ⬅ NEW
from glob import glob           #  ⬅ NEW

package_name = 'bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),

    # ────────────────────────────────────────────────────────────────
    # Tell ament where to copy your launch files at install time
    # ────────────────────────────────────────────────────────────────
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),        # ⬅ NEW
         glob(os.path.join('launch', '*.launch.py'))),         # ⬅ NEW
        # If you later add YAML‑config or RViz files, add another
        # ( os.path.join('share', package_name, 'config'), glob('config/*') ),
    ],

    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='bauerjo@ethz.ch',
    description='Launch + bring‑up files',
    license='TODO: License declaration',
    tests_require=['pytest'],

    # No console scripts for a pure bring‑up package
    entry_points={'console_scripts': []},
)