#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
#1. 导入消息类型
from std_msgs.msg import String, UInt32
#从村庄接口服务类中导入借钱服务
from village_interfaces.srv import BorrowMoney

class BaiPiaoNode(Node):
    """
    创建一个白嫖结点，并在初始化时输出一句话
    """
    def __init__(self, name):
       super().__init__(name)
       self.get_logger().info("大家好，我是白嫖党{}".format(name))
       self.sub_novel = self.create_subscription(String,"sexy_girl",self.topic_callback,10)
       self.borrow_money_client_ = self.create_client(BorrowMoney, "borrow_money")


    def topic_callback(self,msg):
       """
       话题回调函数
       :return:
       """
       self.get_logger().info('朕已白嫖：{}'.format(msg.data))

    def borrow_respoonse_callback(self,response):
        """
        借钱结果回调
        """
        # 打印一下信息
        result = response.result()
        if result.success == True:
            self.get_logger().info("果然是亲弟弟，借到%d,吃麻辣烫去了" % result.money)
        else:
            self.get_logger().info("害，连几块钱都不借,我还是不是他亲哥了，世态炎凉呀")

    def borrow_money_eat(self):
        """
        借钱吃麻辣烫函数
        """
        #打印一句话
        self.get_logger().info("找我弟借钱吃麻辣烫喽")
        #等待服务启动，每1s检查一次，如果服务没有启动，则一直循环
        while not self.borrow_money_client_.wait_for_service(1.0):
            self.get_logger().warn("我弟不在线，我再等等。")
        # 构建请求内容
        request = BorrowMoney.Request()
        #将当前节点名称作为借钱者姓名
        request.name = self.get_name()
        #借钱金额10元
        request.money = 10
        #发送异步借钱请求，借钱成功后就调用borrow_respoonse_callback()函数
        self.borrow_money_client_.call_async(request).add_done_callback(self.borrow_respoonse_callback)



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
    node.borrow_money_eat()
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy