import requests

url = "http://20.41.122.250:8080/predict"
image_path = "./test-dataset/3.jpeg"  # 전송할 이미지 경로

with open(image_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

if response.status_code == 200:
    result = response.json()
    print("Response:", result)
else:
    print(f"Error: {response.status_code}, {response.text}")
