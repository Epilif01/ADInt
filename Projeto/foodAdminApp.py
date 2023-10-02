from xmlrpc import client

proxy = client.ServerProxy("http://localhost:8001/api")

print("Welcome to the Food Admin App")
print("Please authenticate yourself")
username = input("Username: ")
print("Welcome %s" % username)

while True:
    print("Please select an option:")
    print("1. Create restaurant")
    print("2. My Restaurants")
    print("3. Update menu")
    print("4. Show reviews")
    print("5. Exit")
    option = input("Option: ")
    try:
        if option == "1":
            name = input("Restaurant name: ")

            restaurantExists = proxy.validateRestaurant(name, username)
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
                item = input("Item (or empty to finish): ")
                if item == "":
                    break
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
