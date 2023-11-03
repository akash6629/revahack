import rclpy
 from aabcgs_telepo_receiver.msg
import MyCommand
 def command_callback(msg):
     print(f"Received command:{msg.command}")
 def main(args=None):
     rclpy.init(args=args)
     node = rclpy.create_node('receiver node')
     subscription = node.create_subscription(MyCommand, 'command_topic', command_callback)
     try:
         rclpy.spin(node)
     except KeyboardInterrupt:
         pass
     node.destroy_node()
     rclpy.shutdown()
 if _name_ == '_main_':
    main()
