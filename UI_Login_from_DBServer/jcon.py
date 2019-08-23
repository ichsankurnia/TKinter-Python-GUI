import urllib.request, json

def updateJson():
    # blt = []
    url = "http://security.goes2nobel.com/jsin.php"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode())
    # print(data) # {"user":[{"id":"21","name":"Yahya Abdurrozaq","email":"yahya.abdurr@gmail.com","number":"1316010059","password":"konkoo53"},{"id":"22","name":"Arba Abdul S","email":"arba@gmail.com","number":"1316010069","password":"123"},{"id":"23","name":"Bachtiar Pramadi","email":"bepe@gmail.com","number":"1316010057","password":"bepe"},{"id":"24","name":"Habibburahman","email":"habib@gmail.com","number":"1316010078","password":"123"},{"id":"25","name":"Ichsan Kurniawan","email":"ichsan@gmail.com","number":"1316010006","password":"123"},{"id":"26","name":"Maya Ayuningtyas","email":"maya@gmail.com","number":"1316010079","password":"123"},{"id":"27","name":"Nada Fathimah","email":"nada@gmail.com","number":"1316010063","password":"123"},{"id":"28","name":"Pramitha Retno A","email":"tyas@gmail.com","number":"1316010043","password":"123"},{"id":"29","name":"Raka Priatnanugraha","email":"raka@gmail.com","number":"1316010088","password":"123"},{"id":"30","name":"Tri Irfan","email":"irfan@gmail.com","number":"1316010070","password":"123"}]}

    text=''
    with open("login.txt", "w") as file:
        file.write(text)

    nama = ""
    for i in data["user"]:
        email = i["email"]
        pwd = i['password']
        name = i['name']
        nim = i['number']
        print(i)
        print(email)
        text = email+';'+pwd+';'+name+';'+nim
        with open("login.txt", "a") as file:
            file.write(text + '\n')