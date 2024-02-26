### Install python on your local setup first.

1. Open your cmd or terminal and go to directory ./binancedata/
2. Activate virtual env. If you have windows then type : .env/Scripts/Activate , and if you have macos then : Source sanket/bin/activate
3. Go to data directory cd data and run the server by command. python manage.py runserver

### Start the all 3 websocket

keep all terminals open to run sockets.
1. Open new cmd or terminal and go to directory ./binancedata/
2. Activate virtual env. If you have windows then type : .env/Scripts/Activate , and if you have macos then : Source sanket/bin/activate
3. Go to data directory cd data and run first websocket by command : python manage.py command

1. Open new cmd or terminal and go to directory ./binancedata/
2. Activate virtual env. If you have windows then type : .env/Scripts/Activate , and if you have macos then : Source sanket/bin/activate
3. Go to data directory cd data and run second websocket by command : python manage.py command1

1. Open new cmd or terminal and go to directory ./binancedata/
2. Activate virtual env. If you have windows then type : .env/Scripts/Activate , and if you have macos then : Source sanket/bin/activate
3. Go to data directory cd data and run third websocket by command : python manage.py command3


1. Open new cmd or terminal and go to directory ./binancedata/
2. Activate virtual env. If you have windows then type : .env/Scripts/Activate , and if you have macos then : Source sanket/bin/activate
3. Go to data directory cd data and run schedule to capture updatetd data by command : python manage.py onehr