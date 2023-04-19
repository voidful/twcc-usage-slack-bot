import datetime
import json
import os
import time

import requests
import schedule
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
API_KEY_VALUE = os.environ['API_KEY_VALUE']
PROJECT_IDS = os.environ['PROJECT_IDS'].split(',')
slack_client = WebClient(token=SLACK_BOT_TOKEN)


def get_daily_usage(project_id):
    url = f"https://apigateway.twcc.ai/api/v3/k8s-D-twcc/projects/reports/?project={project_id}"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'x-api-host': 'k8s-D-twcc',
        'x-api-key': API_KEY_VALUE
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text


def post_daily_usage_to_slack():
    for project_id in PROJECT_IDS:
        try:
            daily_usage = get_daily_usage(project_id)
            usage_data = json.loads(daily_usage)
            today = datetime.date.today()

            user_usage = {}
            for project in usage_data["projects"]:
                for k8s in project["detail"]["K8S"]:
                    start_time = datetime.datetime.fromisoformat(k8s["start_time"].replace("Z", "+00:00")).date()
                    if start_time == today:
                        user_id = k8s["user"]["id"]
                        user_display_name = k8s["user"]["display_name"]
                        gpu_hour = k8s["gpu_hour"]

                        if user_id not in user_usage:
                            user_usage[user_id] = {
                                "display_name": user_display_name,
                                "gpu_hour": gpu_hour,
                            }
                        else:
                            user_usage[user_id]["gpu_hour"] += gpu_hour

            for user_id, usage in user_usage.items():
                slack_client.chat_postMessage(
                    channel=SLACK_CHANNEL,
                    text=f"{usage['display_name']} 在專案 {project_id} 中今天的 GPU 使用量為：{usage['gpu_hour']} 小時",
                )
        except SlackApiError as e:
            print(f"Error posting message: {e}")


post_daily_usage_to_slack()
schedule.every().day.at("00:00").do(post_daily_usage_to_slack)

while True:
    schedule.run_pending()
    time.sleep(60)
