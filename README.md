# chatbot_facebook

Chatbot do facebook hospedado no Heroku, o chatbot é um web service desenvolvido em python que fica recebendo todas as requisições q são enviadas via API do Facebook pelos usuários através do chat.

O usuário passa um título da notícia que ele acredita ser Fake, e o bot envia esse título para uma API previamente desenvolvida que está hospedada na AMS, ele faz a verificação desse título e retorna para o usuário no facebook se o título da notícia é de fato referente a alguma Fake News.
