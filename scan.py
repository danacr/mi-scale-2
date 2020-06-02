#!/usr/bin/env python3

from bluepy.btle import DefaultDelegate

import fitbit
import ops_genie as ops
import os


class ScanDelegate(DefaultDelegate):
    def __init__(self, args):
        DefaultDelegate.__init__(self)
        self.mac_address = os.environ['mac']
        self.is_verbose = args.verbose > 0
        self.last_raw_data = None

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if self.mac_address == dev.addr.upper():
            self.parseData(dev)

    def parseData(self, dev):
        if self.is_verbose:
            print('Device %s is %s, rssi: %d dBm, connectable: %s.' %
                  (dev.addr, dev.addrType, dev.rssi, dev.connectable))

        # 1 - flags, 2 - Incomplete 16b Services, 255 - Manufacturer, 22 - 16b Service Data, 9 - Complete Local Name
        SERVICE_DATA = 22  # [1d18828809e4070310112302]

        for (adtype, desc, value) in dev.getScanData():
            if adtype == SERVICE_DATA and value.startswith('1d18'):
                raw_data = bytes.fromhex(value[4:])
                if raw_data == self.last_raw_data:
                    if self.is_verbose:
                        print("skip duplicate data")
                    return

                is_stabilized = (raw_data[0] & (1 << 5)) != 0
                is_weight_removed = (raw_data[0] & (1 << 7)) != 0
                self.last_raw_data = raw_data

                if is_stabilized is True and is_weight_removed is False:
                    weight = int.from_bytes(
                        raw_data[1:3], byteorder='little') / 100

                    if (raw_data[0] & (1 << 1)) != 0:  # kg
                        weight /= 2  # catty to kg
                    print(weight)  # output: 74.7
                    if float(os.environ['lower']) <= weight <= float(os.environ['upper']):
                        authd_client = fitbit.Fitbit(os.environ['client_key'], os.environ['client_secret'],
                                                     access_token=os.environ['access_token'], refresh_token=os.environ['refresh_token'], system=os.environ['unit_system'])
                        authd_client.user_profile_update(
                            data={u'weight': weight})
                        print("Uploaded data")
                        alert = ops.Alert()
                        response = alert.create_alert(weight)
                        alert_id = response.id
                        result = response.retrieve_result()
                        alert.get_alert(alert_id)
                        alert.close_alert(alert_id)
