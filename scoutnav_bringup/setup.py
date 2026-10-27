from setuptools import setup
from glob import glob
import os
package_name = "scoutnav_bringup"
setup(
    name=package_name, version="0.1.0", packages=[],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "worlds"), glob("worlds/*")),
    ],
    install_requires=["setuptools"], zip_safe=True,
    maintainer="ScoutNav Contributors",
    maintainer_email="maintainer@example.com",
    description="Launch files for ScoutNav simulation.", license="MIT",
)
