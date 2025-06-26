import io
import torch
from PIL import Image
from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient
from torchvision import transforms
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -- Azure Blob Storage 설정 --
connection_string = "DefaultEndpointsProtocol=https;AccountName=netzero25account;AccountKey=RZowAl7S5wZijzYGJlfvA1tsJSjgxAPc3kypCbdl4QpKslvbJS9I65d8BbLb32zsF2eJeUHj4DfU+ASt0s6B8g==;EndpointSuffix=core.windows.net"
container_name = "netzero-container"
blob_name = "full_model.pth"
local_model_path = "./full_model_downloaded.pth"

# -- 모델 다운로드 함수 --
def download_model():
    blob_service = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)
    with open(local_model_path, "wb") as file:
        download_stream = blob_client.download_blob()
        file.write(download_stream.readall())
    print("✅ 모델 다운로드 완료")

# -- 모델 로드 --
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
download_model()
model = torch.load(local_model_path, map_location=device, weights_only=False)
model.to(device)
model.eval()


# -- 이미지 전처리 --
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# -- 예측 함수 --
def predict(image_bytes, threshold=0.5):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img_tensor)
        prob = torch.sigmoid(output).item()

    plugged_in = prob <= threshold
    return {"score": round(prob, 4), "result": "true" if plugged_in else "false"}

# -- Flask 라우트 --
@app.route("/predict", methods=["POST"])
def predict_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    image_bytes = file.read()
    result = predict(image_bytes)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)