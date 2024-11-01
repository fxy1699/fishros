import rclpy
from rclpy.node import Node
from dynamic_reconfigure.server import Server
from fishbot_description.srv import DynamicReconfigure  # 替换your_package_name为实际的包名

class DynamicReconfigureServer(Node):
    def __init__(self):
        super().__init__('dynamic_reconfigure_server')
        self.server = Server(DynamicReconfigure.Config, self.config_callback)

    def config_callback(self, config, level):
        self.get_logger().info('Reconfigure Request: %s', config)
        speed = config.speed
        # 更新速度
        self.get_node('rotate_fishbot_wheel').update_speed([speed, speed])
        return config

def main(args=None):
    rclpy.init(args=args)
    node = DynamicReconfigureServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()