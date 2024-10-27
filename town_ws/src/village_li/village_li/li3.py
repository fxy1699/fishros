#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
#1. 导入消息类型
from std_msgs.msg import String, UInt32


class BaiPiaoNode(Node):
    """
    创建一个白嫖结点，并在初始化时输出一句话
    """
    def __init__(self, name):
       super().__init__(name)
       self.get_logger().info("大家好，我是白嫖党{}".format(name))
       self.sub_novel = self.create_subscription(String,"sexy_girl",self.topic_callback,10)

    def topic_callback(self,msg):
       """
       话题回调函数
       :return:
       """
       self.get_logger().info('朕已白嫖：{}'.format(msg.data))


def main(args=None):
    """
    ros2运行该节点的入口函数
    1. 导入库文件
    2. 初始化客户端库
    3. 新建节点
    4. spin循环节点
    5. 关闭客户端库
    """
    rclpy.init(args=args) # 初始化rclpy
    node = BaiPiaoNode("li3")  # 新建一个节点
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy