import requests

# url = "https://api.openai.com/v1/chat/completions"
url = "https://api.openai.com/v1/images/generations"

# "model":"gpt-3.5-turbo-0301","messages": [{"role": "user", "content": "神斗士星矢是谁创作的"}]
payload = '''{
  "prompt": "以天气,龙黑洞,白虎为题材生成一张中国风的图片",
  "n": 2,
  "size": "1024x1024"
}'''

payload = payload.encode("utf-8")
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15',
    'Content-Type': 'application/json',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Authorization': 'Bearer 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',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
# openai.organization = "org-9FucxtwNZHeS2hHTwnkj5brx"
# openai.api_key = "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"
# print(openai.Chat.)
