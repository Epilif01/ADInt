from xmlrpc import client

proxy = client.ServerProxy("http://localhost:8002/api")

print("Welcome to the Room Admin App")
""" print("Please authenticate yourself")
username = input("Username: ")
print("Welcome %s" % username)
 """
while True:
    print("Please select an option:")
    print("1. Create room")
    print("2. My Rooms")
    print("3. Update schedule")
    print("4. Update schedule from Fenix")
    print("5. Exit")
    option = input("Option: ")
    try:
        if option == "1":
            name = input("Room name: ")
            room_id = input("Room id: ")
            #validate room_id format

            roomExists = proxy.validateRoom(room_id)
            if roomExists == True:
                print("That room already exists")
                continue
            qrcode = proxy.createRoom(name, room_id)
            print("Get you QRCode at: %s in the next 2 minutes" % qrcode)
        elif option == "2":
            print(proxy.myRooms())
        elif option == "3":
            room_id = input("room_id: ")
            roomExists = proxy.validateRoom(room_id)
            if roomExists == False:
                print("There is no room with that id")
                continue
            weekday = input("Weekday: ")
            if weekday == "":
                break
            slot_start = input("Start time: ")
            if slot_start == "":
                break
            slot_end = input("End time: ")
            if slot_end == "":
                break
            data = {
                "weekday": weekday,
                "slot_start": slot_start,
                "slot_end": slot_end
            }
            proxy.updateSchedule(room_id, data)
        elif option == "4":
            room_id = input("room_id: ")
            roomExists = proxy.validateRoom(room_id)
            if roomExists == False:
                print("There is no room with that id")
                continue
            proxy.updateFromFenix(room_id)
        elif option == "5":
            break
        else:
            print("Invalid option")
    except client.ProtocolError as err:
        print("A protocol error occurred")
        print("URL: %s" % err.url)
        print("HTTP/HTTPS headers: %s" % err.headers)
        print("Error code: %d" % err.errcode)
        print("Error message: %s" % err.errmsg)
    except client.Fault as err:
        print("RPC error occurred")
        print("Error code: %d" % err.faultCode)
        print("Error message: %s" % err.faultString)
        pass
