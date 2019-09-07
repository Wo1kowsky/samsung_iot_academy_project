# keyboards for VK chat
import json

menu = json.dumps({
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Управление"
            },
            "color": "positive"
        }
        ],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"3\"}",
                "label": "Помощь"
            },
            "color": "primary"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"4\"}",
                    "label": "О нас"
                },
                "color": "primary"
            }
        ]
    ]
}, ensure_ascii=False).encode('utf-8')

options = json.dumps({
    "one_time": True,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Добавить устройство"
            },
            "color": "positive"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Открепить устройство"
                },
                "color": "negative"
            }
        ],
    ]
}, ensure_ascii=False).encode('utf-8')
