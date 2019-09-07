def do_connect(sta_if, ssid, password):
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def do_disconnect(sta_if):
    sta_if.active(False)
