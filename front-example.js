// 먼저 axios와 form-data 설치 필요:
// npm install axios form-data

const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const url = "http://127.0.0.1:8080/predict";
const imagePath = "./test-dataset/3.jpeg";

const form = new FormData();
form.append('file', fs.createReadStream(imagePath));

axios.post(url, form, {
  headers: {
    ...form.getHeaders()
  }
})
.then(response => {
  console.log("Response:", response.data);
})
.catch(error => {
  if (error.response) {
    console.error(`Error: ${error.response.status}, ${error.response.data}`);
  } else {
    console.error("Error:", error.message);
  }
});
