from xmlrpc import client
import datetime as dt

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
            # validate room_id format

            roomExists = proxy.validateRoom(room_id)
            if roomExists == True:
                print("That room already exists")
                continue
            qrcode = proxy.createRoom(name, room_id)
            print("Get you QRCode at: %s in the next 2 minutes" % qrcode)
        elif option == "2":
            print(proxy.myRooms())
        elif option == "3":
            data = []
            while True:
                room_id = input("room_id: ")
                roomExists = proxy.validateRoom(room_id)
                if roomExists == False:
                    print("There is no room with that id")
                    continue

                while True:
                    day = input("day: ")
                    try:
                        dt.datetime.strptime(day, "%d/%m/%Y")
                        break
                    except:
                        print("Invalid day")

                while True:
                    slot_start = input("Start time: ")
                    hours = int(slot_start.split(":")[0])
                    minutes = int(slot_start.split(":")[1])
                    if hours >= 0 and hours <= 23 and minutes >= 0 and minutes <= 59:
                        break

                    print("Invalid time")

                while True:
                    slot_end = input("End time: ")
                    hours = int(slot_end.split(":")[0])
                    minutes = int(slot_end.split(":")[1])
                    if hours >= 0 and hours <= 23 and minutes >= 0 and minutes <= 59:
                        break

                    print("Invalid time")

                while True:
                    type = input("Type: ")
                    if type in ["GENERIC", "LESSON", "EXAM"]:
                        break

                    print("Invalid type")

                if type == "GENERIC":
                    name = input("Name: ")
                    course_id = None

                else:
                    name = input("Course name: ")
                    while True:
                        course_id = input("Course id: ")
                        if course_id.isdigit():
                            break

                        print("Invalid course id")

                data.append(
                    {
                        "day": day,
                        "slot_start": slot_start,
                        "slot_end": slot_end,
                        "name": name,
                        "type": type,
                        "course_id": course_id,
                    }
                )

                loop = input("Add another event? ([Y]/n): ")
                if loop == "n":
                    break

            proxy.updateSchedule(room_id, data)
            print("Schedule updated")

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
