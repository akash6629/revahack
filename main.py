import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, select, termios, tty

msg = """
Control Your Rover!
---------------------------
Moving around:
   w
a  s  d
   x

w/x : increase/decrease linear velocity
a/d : increase/decrease angular velocity
s : stop
CTRL-C to quit
"""

class TeleopNode(Node):
    def _init_(self):
        super()._init_('teleop_node')
        self.publisher_ = self.create_publisher(Twist, 'rover/cmd_vel', 10)
        self.msg_ = Twist()
        self.linear_speed_ = 0.5
        self.angular_speed_ = 0.5

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings_)
        return key

    def send_command(self, key):
        if key == 'w':
            self.msg_.linear.x += self.linear_speed_
        elif key == 'x':
            self.msg_.linear.x -= self.linear_speed_
        elif key == 'a':
            self.msg_.angular.z += self.angular_speed_
        elif key == 'd':
            self.msg_.angular.z -= self.angular_speed_
        elif key == 's':
            self.msg_.linear.x = 0.0
            self.msg_.angular.z = 0.0
        else:
            pass
        self.publisher_.publish(self.msg_)

def main(args=None):
    rclpy.init(args=args)
    node = TeleopNode()
    try:
        print(msg)
        while True:
            key = node.get_key()
            if key == '\x03':  # Ctrl-C
                break
            else:
                node.send_command(key)
    except Exception as e:
        print('Error: ', e)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if _name_ == '_main_':
    main()
