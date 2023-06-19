# Ponderada de Supabase

Este repositório se refere à ponderada da semana 7, de integração entre o OpenCV com ROS2 e um file storage no Supabase. O objetivo é salvar os frames de um vídeo no Supabase a partir do ROS2, utilizando um servidor, no caso, em FastAPI.

Para isso, utilizamos três scripts. O "main.py" cria uma servidor em FastAPI no localhost:8000, que se conecta com a minha conta no Supabase e oferece duas rotas: uma para ver a lista de itens no bucket e outra para subir itens, além de salvá-los na pasta "recebidos" deste repositório, por redundância.

Já o script "image_publisher_ros.py" é um publicador ROS2 responsável por acessar o vídeo e enviar frame a frame para um tópico "video_frames". O vídeo em si se encontra na pasta "assets". 

Por fim, o script "enviar.py" cria um subscriber para esse mesmo tópico e recebe os frames. Então, para cada frame, é feita uma requisição para o endereço do servidor na rota de upload. Com isso, fecha-se o ciclo, em que o frame é enviado para o script "main.py" e salvo na pasta "recebidos" e no Supabase.

VÍDEO: https://youtu.be/3p7_sB8lIRk