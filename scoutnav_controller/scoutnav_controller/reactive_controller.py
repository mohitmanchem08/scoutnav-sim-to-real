import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


def choose_command(ranges, stop_m=0.35):
    """Return linear velocity, angular velocity and state for a forward-sector scan."""
    finite = [r for r in ranges if math.isfinite(r) and r > 0.0]
    if not finite:
        return 0.0, 0.0, "FAULT"
    if min(finite) < stop_m:
        return 0.0, 0.55, "TURN"
    return 0.12, 0.0, "FORWARD"


class ReactiveController(Node):
    def __init__(self):
        super().__init__("scoutnav_reactive_controller")
        self.declare_parameter("stop_distance_m", 0.35)
        self.declare_parameter("linear_speed_mps", 0.12)
        self.declare_parameter("turn_rate_rps", 0.55)
        self.declare_parameter("scan_topic", "/scan")
        self.declare_parameter("cmd_topic", "/cmd_vel")
        self.publisher = self.create_publisher(Twist, self.get_parameter("cmd_topic").value, 10)
        self.subscription = self.create_subscription(
            LaserScan, self.get_parameter("scan_topic").value, self.on_scan, 10
        )
        self.last_scan_time = self.get_clock().now()
        self.watchdog = self.create_timer(0.25, self.check_scan_watchdog)

    def publish_command(self, linear, angular):
        msg = Twist()
        msg.linear.x = float(linear)
        msg.angular.z = float(angular)
        self.publisher.publish(msg)

    def on_scan(self, msg):
        self.last_scan_time = self.get_clock().now()
        ranges = []
        for index, value in enumerate(msg.ranges):
            angle = msg.angle_min + index * msg.angle_increment
            if abs(angle) <= math.pi / 4.0:
                ranges.append(value)
        valid = [r for r in ranges if math.isfinite(r) and r > 0.0]
        if not valid:
            self.publish_command(0.0, 0.0)
            self.get_logger().warn("No valid forward-sector scan values; stopping")
            return
        stop_m = float(self.get_parameter("stop_distance_m").value)
        _, _, state = choose_command(valid, stop_m)
        if state == "FORWARD":
            self.publish_command(self.get_parameter("linear_speed_mps").value, 0.0)
        elif state == "TURN":
            self.publish_command(0.0, self.get_parameter("turn_rate_rps").value)
        else:
            self.publish_command(0.0, 0.0)

    def check_scan_watchdog(self):
        age = (self.get_clock().now() - self.last_scan_time).nanoseconds / 1e9
        if age > 0.75:
            self.publish_command(0.0, 0.0)


def main(args=None):
    rclpy.init(args=args)
    node = ReactiveController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.publish_command(0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
