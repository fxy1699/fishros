#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
# 1.导入消息类型JointState
from sensor_msgs.msg import JointState
# from rcl_interfaces.msg import SetParametersResult

import threading
import time

class RotateWheelNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info(f"node {name} init..")
        # 创建并初始化发布者成员属性pub_joint_states_
        self.joint_states_publisher_ = self.create_publisher(JointState,"joint_states", 10) 
        # 初始化数据
        self._init_joint_states()
        self.pub_rate = self.create_rate(30)
        self.thread_ = threading.Thread(target=self._thread_pub)
        self.thread_.start()
        # 初始化参数设置回调函数
        # self.add_on_set_parameters_callback(self.parameter_callback)
    
    # def declare_param_with_range(self,name,value,start,end):
    #     pd = ParameterDescriptor()
    #     pd_range = IntegerRange()
    #     pd_range.from_value = start
    #     pd_range.to_value = end
    #     pd_range.step = 1
    #     pd.integer_range.append(pd_range)
    #     self.declare_parameter(name,value,pd) 
    
    # def parameter_callback(self, parameters):
    #     results = []
    #     for parameter in parameters:
    #         try:
    #             # 获取参数的新值并做处理
    #             new_value = parameter.value
    #             self.get_logger().info(f'参数 {parameter.name} 设置为: {new_value}')
    #             # self.sync_param(parameter.name, new_value)
    #             # 构造参数设置结果
    #             result = SetParametersResult(successful=True)
    #         except Exception as e:
    #             self.get_logger().error(f'设置参数 {parameter.name} 失败: {e}')
    #             result = SetParametersResult(successful=False, reason=str(e))
    #         results.append(result)
    #     return SetParametersResult(successful=True, results=results)

    # def sync_param(self, param_name, param_value):
    #     # 这里实现将参数同步到硬件的逻辑，例如发送命令到摄像头以设置相应的参数
    #     pass
    
    def _init_joint_states(self):
        # 初始左右轮子的速度
        self.joint_speeds = [0.0,0.0]
        self.joint_states = JointState()
        self.joint_states.header.stamp = self.get_clock().now().to_msg()
        self.joint_states.header.frame_id = ""
        # 关节名称
        self.joint_states.name = ['left_wheel_joint','right_wheel_joint']
        # 关节的位置
        self.joint_states.position = [0.0,0.0]
        # 关节速度
        self.joint_states.velocity = self.joint_speeds
        # 力 
        self.joint_states.effort = []

    def update_speed(self,speeds):
        self.joint_speeds = speeds

    def _thread_pub(self):
        last_update_time = time.time()
        while rclpy.ok():
            delta_time =  time.time()-last_update_time
            last_update_time = time.time()
            # 更新位置
            self.joint_states.position[0]  += delta_time*self.joint_states.velocity[0]
            self.joint_states.position[1]  += delta_time*self.joint_states.velocity[1]
            # 更新速度
            self.joint_states.velocity = self.joint_speeds
            # 更新 header
            self.joint_states.header.stamp = self.get_clock().now().to_msg()
            # 发布关节数据
            self.joint_states_publisher_.publish(self.joint_states)
            self.pub_rate.sleep()

def main(args=None):
    rclpy.init(args=args) # 初始化rclpy
    node = RotateWheelNode("rotate_fishbot_wheel")  # 新建一个节点
    node.update_speed([5.0,5.0])
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy