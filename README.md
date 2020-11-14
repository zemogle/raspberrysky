# Raspberry Sky

The purpose of this code is to turn a Raspberry Pi into an all sky camera.

## Software Requirements
- celery
- redis server (this is a bit tricky on a raspberry pi)

## Hardware Requirements
- Raspberry Pi
- PiCamera module

A complete list of components can be found on [my Dark Matter Sheep blog post](http://www.darkmattersheep.uk/blog/the-great-raspberry-pi-all-sky-adventure/).

## Installation

- Install supervisor, if you use a system package it should be installed with autorun enabled (although tied to python2.7 for some reason):
```
sudo apt-get install supervisor
sudo reboot
```

Configure redis as a service (so it autostarts in the background). The [redis](https://redis.io/topics/quickstart) docs are really useful:
 - When you edit `/etc/init.d/redis_6379` change redis-server and redis-cli to `/usr/bin/<NAME>` respectively

Add configs for celery workers
Into `/etc/supervisor/conf.d/celery.conf` put:
```
[program:celery]
directory=/home/pi/raspberrysky
command=/usr/local/bin/celery -A tasks worker -l info
stdout_logfile=/home/pi/celeryd.log
stderr_logfile=/home/pi/celeryd.log
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=600
```
