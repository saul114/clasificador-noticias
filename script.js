document.addEventListener("DOMContentLoaded", function () {
    const textButton = document.getElementById("textButton");
    const fileButton = document.getElementById("fileButton");
    const linkButton = document.getElementById("linkButton");
    const submitButton = document.getElementById("submitButton");

    const textInputContainer = document.getElementById("textInputContainer");
    const fileInputContainer = document.getElementById("fileInputContainer");
    const linkInputContainer = document.getElementById("linkInputContainer");

    const textInput = document.getElementById("textInput");
    const fileInput = document.getElementById("fileInput");
    const linkInput = document.getElementById("linkInput");

    const resultDiv = document.getElementById("result");

    let selectedMethod = null;

    function hideAllInputs() {
        textInputContainer.style.display = "none";
        fileInputContainer.style.display = "none";
        linkInputContainer.style.display = "none";
    }

    textButton.addEventListener("click", function () {
        hideAllInputs();
        textInputContainer.style.display = "block";
        selectedMethod = "text";
    });

    fileButton.addEventListener("click", function () {
        hideAllInputs();
        fileInputContainer.style.display = "block";
        selectedMethod = "file";
    });

    linkButton.addEventListener("click", function () {
        hideAllInputs();
        linkInputContainer.style.display = "block";
        selectedMethod = "link";
    });

    submitButton.addEventListener("click", function () {
        resultDiv.textContent = "Procesando...";
        // Dependiendo del método seleccionado, se envía la petición correspondiente.
        if (selectedMethod === "text") {
            let textValue = textInput.value.trim();
            if (!textValue) {
                resultDiv.textContent = "Por favor, ingresa un texto.";
                return;
            }
            fetch("http://127.0.0.1:5000/predict-text", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: textValue })
            })
            .then(response => response.json())
            .then(data => {
                if (data.category)
                    resultDiv.textContent = "Categoría: " + data.category;
                else
                    resultDiv.textContent = "Error: " + data.error;
            })
            .catch(error => {
                console.error("Error:", error);
                resultDiv.textContent = "Error en la petición.";
            });
        } else if (selectedMethod === "file") {
            if (fileInput.files.length === 0) {
                resultDiv.textContent = "Por favor, selecciona un archivo.";
                return;
            }
            let formData = new FormData();
            formData.append("file", fileInput.files[0]);
            fetch("http://127.0.0.1:5000/upload", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.category)
                    resultDiv.textContent = "Categoría: " + data.category;
                else
                    resultDiv.textContent = "Error: " + data.error;
            })
            .catch(error => {
                console.error("Error:", error);
                resultDiv.textContent = "Error en la petición.";
            });
        } else if (selectedMethod === "link") {
            let linkValue = linkInput.value.trim();
            if (!linkValue) {
                resultDiv.textContent = "Por favor, ingresa una URL.";
                return;
            }
            fetch("http://127.0.0.1:8000/process-url", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url: linkValue })
            })
            .then(response => response.json())
            .then(data => {
                if (data.category)
                    resultDiv.textContent = "Categoría: " + data.category;
                else
                    resultDiv.textContent = "Error: " + data.error;
            })
            .catch(error => {
                console.error("Error:", error);
                resultDiv.textContent = "Error en la petición.";
            });
        } else {
            resultDiv.textContent = "Selecciona un método de ingreso.";
        }
    });
});
