 # Запуск сервиса через Jenkins

 > Технологии: OpenStack, Jenkins, HashiCorp Vault
 
 1. Сборка проекта при помощи maven, архивация артефактов.
 2. Разворачивание инфраструктуры.  
    `heat-orchestration.yaml` - конфигурация используемых ресурсов.  
    `parameters.yaml` - параметры ресурсов.  
    `cloud-formation.py` - скрипт, автоматизирующий создание стека.
    
    Запуск: `cloud-formation.py glezova_weather_bot_infr heat-orchestration.yaml parameters.yaml`
 4. Старт сервиса на созданной инфраструктуре.  
     `sudo systemctl reastart weather-bot`
