import os

import requests
import os


class AlertDispatcher:
    def __init__(self, config, logger, lambda_name):
        self.config = config
        self.logger = logger
        self.lambda_name = lambda_name

    def dispatch_raw_slack(self, sender_id: str, channels: list, text: str):
        try:
            slack_url = self.config.INS_BASE_URI + "/message/raw"

            headers = {
                'Content-Type': "application/json", "Accept": "*/*"
            }
            data_json = {
                "sender_id": self.lambda_name,
                "slack": {
                    "username": sender_id,
                    "channels": channels,
                    "text": f"[{os.getenv('APP_PROFILE') or 'local'}] " + text
                }
            }
            response = requests.post(url=slack_url, headers=headers, json=data_json, verify=False)
            return response.status_code == 200
        except Exception as ex:
            logger.error(ex)
            return False
