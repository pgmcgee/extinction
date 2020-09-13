import sengled

api = sengled.api(
        username="parker@thosemcgees.com",
        password="B.79L[8>8k6T",
        debug=True,
)

devices = api.get_device_details()
print("Devices:")
print(devices)

colored = api.filter_colored_lamps()
print("Colored:")
print(colored)
