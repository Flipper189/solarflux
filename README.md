# solarflux
Send data from the Fronius Solar Inverter API to a InfluxDB.

## description
Solarflux fetches the total current value from a Fronius Solar Inverter and writes it to an InfluxDB every hour.
Tested with Fronius Primo.

## local Setup
- get code "git clone https://github.com/Flipper189/solarflux"
- copy the config file "cp config.json.example config.json
- edit the config file
- install python3
- install python requirements "pip install -r requirements.txt"
- run script "python3 solarflux.py"
- cron job exmaple "0 * * * * your_user_name cd /path/to/the/script_folder && python3 ./solarflux.py"

## docker-compose setup
- get code "git clone https://github.com/Flipper189/solarflux"
- install docker and docker-compose
- copy the config file "cp config.json.example config.json
- edit the config file
- run "docker-compose up --build -d"