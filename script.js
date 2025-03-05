document.getElementById("analyzeButton").addEventListener("click", function () {
    let text = document.getElementById("textInput").value;

    if (text.trim() === "") {
        alert("Por favor, ingresa un texto.");
        return;
    }

    fetch("http://127.0.0.1:5000/predict-text", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        if (data.category) {
            document.getElementById("result").innerText = "Categoría: " + data.category;
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
});

// Procesar archivo .txt
document.getElementById("fileInput").addEventListener("change", function () {
    let file = this.files[0];
    if (!file) return;

    let formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.category) {
            document.getElementById("result").innerText = "Categoría: " + data.category;
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
});

// Procesar URL
document.getElementById("urlButton").addEventListener("click", function () {
    let url = document.getElementById("urlInput").value;

    if (url.trim() === "") {
        alert("Por favor, ingresa una URL.");
        return;
    }

    fetch("http://127.0.0.1:5000/process-url", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.category) {
            document.getElementById("result").innerText = "Categoría: " + data.category;
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
});
