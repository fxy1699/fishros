#!/usr/bin/env python3
import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, UInt32

class SingleDogNode(Node):
    """
    创建一个单身狗节点，并在初始化时输出一句话
    """
    def __init__(self, name):
       super().__init__(name)
       self.get_logger().info("大家好，我是单身狗{}".format(name))
       self.sub_novel = self.create_subscription(String,"sexy_girl",self.topic_callback,10)
       self.pub_money = self.create_publisher(UInt32,"sexy_girl_money",10)

    def topic_callback(self, msg):
       """
       收到话题数据的回调函数
       :return:
       """
       money = UInt32()
       #money.data = random.randint(1, 99)
       money.data = 10
       self.pub_money.publish(money)
       self.get_logger().info('朕已阅：{}, 支付：{}'.format(msg.data, money.data))


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
    node = SingleDogNode("wang2")  # 新建一个节点
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy