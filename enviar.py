# Importa bibliotecas necessárias
import rclpy  
from rclpy.node import Node 
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge  
import cv2 
import httpx
import requests

# Classe para o subscripber do tópico de "video_frames"
class ImageSubscriber(Node):


    def __init__(self):

        super().__init__("image_subscriber")
        
        # Inscreve no tópico
        self.subscription = self.create_subscription(
            Image, "video_frames", self.listener_callback, 10
        )
        self.subscription  

        # Inicializa bridge entre ROS2 e OpenCV
        self.br = CvBridge()

    # Callback para receber os frames
    def listener_callback(self, data):
        
        self.get_logger().info("Receiving video frame")
        
        # Converte mensagem de ROS para imagem em OpenCV
        current_frame = self.br.imgmsg_to_cv2(data)

        # Parâmetros para envio (URL e headers)
        url = "http://127.0.0.1:8000/upload"
        files = [("content", ("frame.png", current_frame, "image/png"))]
        response = requests.request("POST", url, files=files)
        

        if response.status_code == 200:
            print("Frame sent successfully!")
        else:
            print("Failed to send frame. Status code:", response.status_code)

        # Mostra frame 
        cv2.imshow("Camera", current_frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            return

# Inicia nó
def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
