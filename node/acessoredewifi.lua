wificonf = {
  -- verificar ssid e senha
  ssid = "Nem Tenta 2",
  pwd = "ns0tcqdn!@#",
  save = false
}


wifi.sta.config(wificonf)
print("modo: ".. wifi.setmode(wifi.STATION))
wifi.eventmon.register(wifi.eventmon.STA_GOT_IP, function (T) print(wifi.sta.getip()) end)