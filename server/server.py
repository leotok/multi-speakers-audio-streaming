import json
import paho.mqtt.client as mqtt
from flask import Flask, render_template, redirect, url_for, request
from song import AudioHandler, StreammingThread
from node_net import NodeNet, Node


app = Flask(__name__)
threads = []

################################
#         Web views
################################

@app.route('/')
def index():
    return render_template('home.html', nodes=node_net.get_nodes())

@app.route('/stream', methods=['POST'])
def start():
    
    # TODO: mostrar no html os nos que ja sao vizinhos de cada no dentro do value do input

    if len(threads) == 0:
        for k, v in request.form.items():
            neighbours = v.split(',')
            node_number = k.split('_')[1]
            node_net.add_neighbours_to_node(node_number, neighbours)

        thread = StreammingThread(1, client, audio)
        thread.start()
        threads.append(thread)

    edge_list = []
    for v, edges in node_net.graph.items():
        print edges
        for e in edges:
            edge_list.append({"from":v, "to":e})
    print edge_list

    return render_template('streaming.html', song_name=audio.current_song["name"], nodes=node_net.get_nodes(), edges=edge_list)


@app.route('/stop')
def stop():
    if len(threads) == 1:
        threads[0].stop()
        del threads[0]
    return redirect(url_for('index'))


################################
#         Mqtt handlers
################################
    
def handle_node_connect(client, userdata, msg):
    print "Handle node connect..."

    data = json.loads(msg.payload)
    node = node_net.add_node(data["number"], data["name"])
    print "Added " + str(node)

def handle_node_sensor(client, userdata, msg):
    print("Handle node sensor...")
    
    # TODO: receber informacao de proximidade de algum sensor
    # e avisar os sensores vizinhos que devem aumentar a musica
    # pegar vizinhos pelo node_net.graph
    # ex:
    #   node_number = ...
    #   data = {
    #       'node': node_number,
    #       'neighbours': []
    #   }
    # 
    #   for v in node_net.graph[node_number]:
    #       data["neighbours"].append(v)
    # 
    #   client.publish("node/neighbours", json.dumps(data))
    


def on_message(client, userdata, msg):
    topics_subscribed = {
        "node/connect": handle_node_connect,
        "node/sensor": handle_node_sensor,
    }

    try:
        callback = topics_subscribed[msg.topic]
        callback(client, userdata, msg)
    except KeyError:
        pass

def on_connect(client, userdata, flags, rc):
    # subscribed pelo server

    client.subscribe('node/connect')
    client.subscribe('node/sensor')

    # subscribed pelos nodes

    # client.subscribe('node/neighbours')
    # client.subscribe('song/info')
    # client.subscribe('song/stream')


if __name__ == '__main__':

    hostname = '127.0.0.1'
    port = 1883
    keep_alive = 60

    node_net = NodeNet()
    audio = AudioHandler()

    # Start web server with mqtt

    client = mqtt.Client()
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(hostname, port, keep_alive)
    client.loop_start()

    app.run(host='127.0.0.1', port=8000, debug=True)
