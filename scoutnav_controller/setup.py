from setuptools import setup
package_name = "scoutnav_controller"
setup(
    name=package_name, version="0.1.0", packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"], zip_safe=True,
    maintainer="ScoutNav Contributors",
    maintainer_email="maintainer@example.com",
    description="Simple reactive controller for ScoutNav simulation.",
    license="MIT",
    entry_points={"console_scripts": [
        "reactive_controller = scoutnav_controller.reactive_controller:main",
    ]},
)
