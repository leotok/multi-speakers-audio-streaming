local List = require "list"

-- ****************************************************************************
--                     Mqtt Callbacks
-- ****************************************************************************

local function connect_node(c)
  c:publish("node/connect", '{ "number": '..NODE_ID..', "name": "" }',0,0, 
            function(client) 
                print("Connected node to server!") 
            end)
end

local function handle_stream(data)
  List.pushleft(chunkList, data)
  data = nil
end

local function publish_sensor_date(c, origin)
    -- TODO: publicar informacao do sensor PIR para o servidor determinar que vizinhos avisar
end

function conectado(client)
  print("conectado")
  connect_node(client)
  
  -- TODO: tratar cada um dos topicos recebidos do servidor
  
  client:subscribe({["song/stream"]=0,["song/info"]=1}, function(conn) print("subscribe ok") end)
  
  -- client:subscribe("node/neighbours", 0, printContent)
  
end

local function handlePIR(presence)
  if sensedPresence == false and presence == 1 then
    volume = 1
    sensedPresence = true
    m:publish("node/sensor", 
      "{ 'node': "..NODE_ID..", 'sensedPresence': 'YES' }")
  elseif sensedPresence == true and presence == 0 then
    volume = 0
    sensedPresence = false
    m:publish("node/sensor", 
      "{ 'node': "..NODE_ID..", 'sensedPresence': 'NO' }")
  end
end

-- ****************************************************************************
--                        PCM Callbacks
-- ****************************************************************************

local function cb_drained(d)
  -- uncomment the following line for continuous playback
  d:play(pcm.RATE_8K)
end

local function cb_stopped(d)
  print("playback stopped")
  file.seek("set", 0)
end

local function cb_paused(d)
  print("playback paused")
end

local function fetch_data(drv) 
  if chunkList == nil then
    return nil
  end

  if List.count(chunkList) < 18 and start == true then
    return nil
  else
    start = false
  end

  -- if List.count(chunkList) < 12 and start == false then
  --   start = true
  -- end

  if collectgarbage("count")*1024 > 15000 then 
    print(collectgarbage("count")*1024)
    collectgarbage("step", 400)
    collectgarbage("collect")
  end

  return List.popright(chunkList)
end

-- ****************************************************************************
--                        Main
-- ****************************************************************************

local function main()
  local hostname = "192.168.100.101" -- ip local do computador
  local port = 1883
  NODE_ID = 3 -- deve variar de node pra node

  chunkList = List.new()
  volume = 0
  sensedPresence = false
  start = true

  -- gpio.trig(1, "both", function(level) print(level) end)

  local m = mqtt.Client("no3", 123)

  m:connect(hostname, port, 0, conectado, 
      function(client, reason) 
          print("failed reason: "..reason) 
      end
  )

  m:on("message", function(client, topic, data)

    if topic == "song/stream" then

      -- print("stream")
      handle_stream(data)
      data = nil

    elseif topic == "song/info" then

      print(data)
    
    elseif topic == "node/neighbours" then
      print(data)
    end
  end)


  local drv = pcm.new(pcm.SD, 1)
   
   -- fetch data in chunks of FILE_READ_CHUNK (1024) from file
  drv:on("data", fetch_data)

   -- get called back when all samples were read from the file
  drv:on("drained", cb_drained)
   
  drv:on("stopped", cb_stopped)
  drv:on("paused", cb_paused)

  drv:play(pcm.RATE_8K)

end


wificonf = {
  -- verificar ssid e senha
  ssid = "Nem Tenta 2",
  pwd = "ns0tcqdn!@#",
  save = false
}

wifi.sta.config(wificonf)
print("modo: ".. wifi.setmode(wifi.STATION))

wifi.eventmon.register(wifi.eventmon.STA_GOT_IP, 
    function (T) 
      print(wifi.sta.getip()) 
      main()
    end
  )

