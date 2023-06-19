
# Importa bibliotecas necessárias
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

# Classe de publicador de imagem, a partir do vídeo

class ImagePublisher(Node):

    def __init__(self):
        super().__init__('image_publisher')

        # Cria publicador no tópico "video_frames"
        self.publisher_ = self.create_publisher(Image, 'video_frames', 10)

        # Frequência das publicações
        timer_period = 0.1

        # Cria o timer
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Acessa o vídeo
        self.cap = cv2.VideoCapture('./assets/siu.mp4')

        # Cria uma ponte entre o ROS2 e o OpenCV
        self.br = CvBridge()

    # Callback para processar cada frame do vídeo (a cada ciclo do timer)
    def timer_callback(self):

        # Lê frame
        ret, frame = self.cap.read()

        # Reinicia vídeo se ele tiver acabado
        if not ret:
            self.get_logger().info("Video seems to be over. Restarting...")
            self.cap = cv2.VideoCapture('./assets/siu.mp4')
            return

        # Publica imagem no tópico
        self.publisher_.publish(self.br.cv2_to_imgmsg(frame))

        self.get_logger().info('Publishing video frame')

# Inicializa nó


def main(args=None):

    rclpy.init(args=args)

    image_publisher = ImagePublisher()

    rclpy.spin(image_publisher)

    image_publisher.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
