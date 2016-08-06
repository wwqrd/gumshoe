needs_wifi = True
update_rate = 120 * 1000

utils = __import__("apps/gumshoe/utils")

def tick():
    print("whereami tick")
    utils.store_location()
    print("whereami tick done")
