#!/usr/bin/env python3

import base64
import fitbit
import ops_genie as ops
import os
import requests


class Upload:
    def upload_weight(self, weight):
        authPlain = os.environ['client_key'] + \
            ':' + os.environ['client_secret']

        authBytes = base64.b64encode(authPlain.encode("utf-8"))
        authStr = str(authBytes, "utf-8")

        headers = {
            'Authorization': 'Basic ' + authStr,
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': os.environ['refresh_token']
        }

        response = requests.post(
            'https://api.fitbit.com/oauth2/token', headers=headers, data=data)

        data = response.json()

        os.environ['refresh_token'] = data['refresh_token']
        f = open('refresh_token', 'w')
        f.write(data['refresh_token'])

        authd_client = fitbit.Fitbit(os.environ['client_key'], os.environ['client_secret'],
                                     access_token=data['access_token'], refresh_token=data['refresh_token'], system=os.environ['unit_system'])
        authd_client.user_profile_update(
            data={u'weight': weight})
        print("Uploaded data")
        alert = ops.Alert()
        response = alert.create_alert(weight)
        alert_id = response.id
        result = response.retrieve_result()
        alert.get_alert(alert_id)
        alert.close_alert(alert_id)
