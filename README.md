# Multi-Speaker Wireless Audio Streaming

## Requirements

- NodeMCU ESP8266
- Speakers
- PIR sensors
- Python 2.7 installed

#### Node firmware

Make sure your NodeMCU firmware has the PCM and MQTT modules. Otherwise, download a new build on https://nodemcu-build.com/ and flash it following this [tutorial](https://nodemcu.readthedocs.io/en/master/en/flash/).

## Install
- On MacOSX:
```
$ brew install mosquitto

$ pip install -r requirements.txt
```

## Running

- Call the following on your shell to start the Mosquitto broker on localhost:1883:
```
$ mosquitto
```

- Run ```server.py``` to start the application
```
$ python server.py
```

## Example

- With both the mosquitto broker and the ```server.py``` running, access the web interface at http://localhost:8000 and
on a new terminal window, call the following commands to connect 3 nodes:
```
$ mosquitto_pub -d -t node/connect -m '{ "number": 1, "name": "Room A" }'

$ mosquitto_pub -d -t node/connect -m '{ "number": 2, "name": "Room B" }'

$ mosquitto_pub -d -t node/connect -m '{ "number": 3, "name": "Room C" }'
```
Refresh the page and you should see the nodes there.
Now, start these two subscribers on new terminal windows:

```
$ mosquitto_sub -d -t song/info

$ mosquitto_sub -d -t song/stream
```
and click on "Start stream".
You should see the results being printed on the subscribers window.

## Topics

- ```song/info```:

Returns information about the song that is playing.

- ```song/stream```

Returns chunks of data of the song that is being streamed.

- ```node/connect```

Adds a node to the node network

- ```node/sensor```

Nodes publish their sensor data to this topic.

- ```node/neighbours```

The server returns each node's neighbours.


