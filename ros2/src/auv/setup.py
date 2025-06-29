from setuptools import setup

package_name = 'auv'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='wiredauv2024',
    maintainer_email='reaf.tamu@gmail.com',
    description='AUV 2024-25',
    license='No license',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'vn_pub = auv.vn_pub:main',
        'cam_pub = auv.cam_pub:main',
        'ms_pub = auv.ms_pub:main',
        'ping_pub = auv.ping_pub:main',
        ],
    },
)
