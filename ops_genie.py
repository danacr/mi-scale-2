#!/usr/bin/env python3

import opsgenie_sdk
import os


class Alert:
    def __init__(self):
        self.conf = self.conf = opsgenie_sdk.configuration.Configuration()
        self.conf.host = 'https://api.eu.opsgenie.com'
        self.conf.api_key['Authorization'] = os.environ['ops_genie']

        self.conf.debug = False

        self.conf.retry_count = 5
        self.conf.retry_http_response = ['4xx', '5xx']
        self.conf.retry_delay = 2
        self.conf.retry_enabled = True

        self.api_client = opsgenie_sdk.api_client.ApiClient(
            configuration=self.conf)
        self.alert_api = opsgenie_sdk.AlertApi(api_client=self.api_client)

    def create_alert(self, weight):
        body = opsgenie_sdk.CreateAlertPayload(
            message='Uploaded weight',
            alias='uploaded_weight',
            description=weight,
            priority='P5'
        )

        try:
            create_response = self.alert_api.create_alert(
                create_alert_payload=body)
            print(create_response)
            return create_response
        except opsgenie_sdk.ApiException as err:
            print("Exception when calling AlertApi->create_alert: %s\n" % err)

    def get_alert(self, alert_id):
        try:
            alert_response = self.alert_api.get_alert(
                identifier=alert_id, identifier_type='id')
            print(alert_response)
            return alert_response
        except opsgenie_sdk.ApiException as err:
            print("Exception when calling AlertApi->get_alert: %s\n" % err)

    def close_alert(self, alert_id):
        body = opsgenie_sdk.CloseAlertPayload(note='Example Closed')
        try:
            close_response = self.alert_api.close_alert(
                identifier=alert_id, close_alert_payload=body)
            print(close_response)
            return close_response
        except opsgenie_sdk.ApiException as err:
            print("Exception when calling AlertApi->close_alerts: %s\n" % err)
