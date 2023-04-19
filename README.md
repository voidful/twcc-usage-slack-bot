# TWCC GPU Usage Notification Slack Bot

本專案用於定期將台灣雲端運算中心（TWCC）上 GPU 使用量通知到 Slack 頻道。

## 前置準備

1. 取得 TWCC API Key：請參考 [TWCC 文件：如何取得 API Key](https://docs.twcc.ai/docs/user-guides/twcc/general/api-keys/)。

2. 取得專案 ID：請參考 [TWCC 文件：取得專案詳細資訊](https://docs.twcc.ai/docs/api/CCS/get-project-detail)。

3. 創建 Slack Bot 並取得 Token：
   - 前往 <https://api.slack.com/apps> 並創建一個新的應用程式。
   - 在 "Add features and functionality" 中選擇 "Bots"，然後點擊 "Set up a bot"。
   - 在 "OAuth & Permissions" 頁面中，為您的機器人添加 `chat:write` 和 `chat:write.public` 權限，然後重新安裝應用程式以獲取新的權杖。
   - 將您的機器人權杖（Bot Token）保存在一個安全的地方。憑證應該是以 "xoxb-" 開頭的。

4. 獲取 Slack Channel ID：
   - 登錄到您的 Slack 工作區。
   - 轉到您想要獲取 Channel ID 的頻道。
   - 在頻道中，右鍵單擊任意一條消息，然後選擇 "Copy link"。
   - 現在，粘貼該鏈接到任意地方（例如文本編輯器）。這個鏈接將顯示 Channel ID。該鏈接的格式類似於：`https://{team_name}.slack.com/archives/{channel_id}/...`。

## 使用方法

1. 將環境變量設置為您的 Slack Bot Token、Slack Channel ID、TWCC API Key 和專案 ID。以逗號分隔專案 ID。

```bash
export SLACK_BOT_TOKEN=xoxb-xxxxx
export SLACK_CHANNEL=xxxxx
export API_KEY_VALUE=xxxx
export PROJECT_IDS=xxxx,xxxxx # separate project id with ,
```

2. 運行主程式：

```bash
python main.py
```

完成以上步驟後，您的機器人將定期將 TWCC GPU 使用量通知發送到指定的 Slack 頻道。
