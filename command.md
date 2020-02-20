###Linux command kill Process
> lsof -i:5000
> sudo kill -9 <i>PID</i>

###activate venv
> virtualenv venv
> source venv/bin/activate

 deactivate
> deactivate

###Run Server
Change to the parent directory of project/
> ./setup.sh

###flask create db table
open python REPL
> from project import db, create_app
> db.create_all(app=create_app())

###Read SQLite database
install sqlite3
> sqlite3 db.sqlite
> .tables

###Refresh cache in browser
> Linux: Ctrl+Shift+R

###Clear Linux Cache Memory
need to be su
> sudo sync; echo 3 > /proc/sys/vm/drop_caches

###Docker commands

Show running containers information
> docker stats

List Docker images
> docker image ls

Build the container 
> docker build -t password_manager .

Run the container 
> docker run -d -p 5000:5000 password_manager

Delete the container
> docker image rmi -f password_manager

###Self-signed CA
> openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem

###WSGI server - waitress [no HTTPS request support]
> waitress-serve --url-scheme=https --call 'project:create_app'

###Uwsgi [TESTING]
> uwsgi --socket 0.0.0.0:5000 --protocol=http --module project
> uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app

uwsgi --shared-socket 0.0.0.0:443 --uid roberto --gid roberto --https =0,foobar.crt,foobar.key

uwsgi --http 127.0.0.1:5000 --module project:app

uwsgi --shared-socket 0.0.0.0:443 --module project:app --https =0,cert.pem,key.pem

uwsgi -s /tmp/password_manager.sock --manage-script-name --mount /password_manager=project:app


<i>Install the pcre packages</i>
sudo apt-get install libpcre3 libpcre3-dev
pip install uwsgi -I --no-cache-dir