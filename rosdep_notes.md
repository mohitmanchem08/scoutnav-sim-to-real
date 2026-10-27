# Dependency notes

Target ROS 2 Jazzy on Ubuntu 24.04 with Gazebo Harmonic. Install `ros_gz_sim`, `ros_gz_bridge`, Xacro and related integration packages from the Jazzy-compatible official repositories. Gazebo/ROS integration package names and launch behavior can evolve; verify the installed package versions.

The included launch and robot description are a concrete starting implementation, but the simulation must be built and run in the target environment and may need package-version-specific integration fixes before it can be described as operational. Do not claim a successful Gazebo run until observed.
