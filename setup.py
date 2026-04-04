from setuptools import setup
import os
from glob import glob

package_name = 'f1car_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
        (os.path.join('share', package_name, 'worlds'),
            glob('worlds/*.sdf')),
        (os.path.join('share', package_name, 'maps'),
            glob('maps/*')),
        (os.path.join('share', package_name, 'config'),
            glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='delia',
    maintainer_email='delia@todo.todo',
    description='F1 car simulation with ROS2 and Gazebo',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)
