from xmlrpc import client

proxy = client.ServerProxy("http://localhost:8001/api")

print("Welcome to the Food Admin App")
print("Please authenticate yourself")
username = input("Username: ")


print("\n\nWelcome %s!" % username)

while True:
    print("\nPlease select an option:")
    print("1. Create restaurant")
    print("2. My Restaurants")
    print("3. Update menu")
    print("4. Show reviews")
    print("5. Exit")
    option = input("Option: ")
    print("\n")
    try:
        if option == "1":
            name = input("Restaurant name: ")
            room_id = input("room_id")

            restaurantExists = proxy.validateRestaurant(name, room_id)
            if restaurantExists == True:
                print("That restaurant already exists")
                continue
            proxy.createRestaurant(name, username)
        elif option == "2":
            print(proxy.myRestaurants(username))
        elif option == "3":
            name = input("Restaurant name: ")
            restaurantExists = proxy.validateRestaurant(name, username)
            if restaurantExists == False:
                print("You do not own a restaurant with that name")
                continue
            menu = []
            while True:
                item = input("Item (or type 'close' to finish): ")
                if item == "close":
                    break
                elif item == "":
                    continue
                menu.append(item)
            proxy.updateMenu(name, menu)
        elif option == "4":
            name = input("Restaurant name: ")
            restaurantExists = proxy.validateRestaurant(name, username)
            if restaurantExists == False:
                print("You do not own a restaurant with that name")
                continue
            print(proxy.showReviews(name))
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
