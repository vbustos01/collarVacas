import json, uos

#uos.mount("/")
f = open("yeison.txt", "w")

#caca = ("sdfdfsd","sdffgfg","pussy", "killer", "iter")
#json.dump(caca, f)

data = {"hola": 23, "fg": 43, "fgfd": "sddf"}
data2 = {"o": 2334, "dic": data}
json.dump(data2, f)

f.close()

f = open("yeison.txt", "r")
datos = json.load(f)

print(datos)
#uos.umount("/")