from xmlrpc import client

proxy = client.ServerProxy("http://localhost:8002/api")

print("Welcome to the Room Admin App")
print("Please authenticate yourself")
username = input("Username: ")
print("Welcome %s" % username)

while True:
    print("Please select an option:")
    print("1. Create room")
    print("2. My Rooms")
    print("3. Update schedule")
    print("4. Exit")
    option = input("Option: ")
    try:
        if option == "1":
            name = input("Room name: ")

            roomExists = proxy.validateRoom(name, username)
            if roomExists == True:
                print("That room already exists")
                continue
            proxy.createRoom(name, username)
        elif option == "2":
            print(proxy.myRooms(username))
        elif option == "3":
            name = input("Room name: ")
            roomExists = proxy.validateRoom(name, username)
            if roomExists == False:
                print("You do not own a room with that name")
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
            proxy.updateSchedule(name, weekday, slot_start, slot_end)
        elif option == "4":
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
