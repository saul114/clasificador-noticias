document.getElementById("analyzeButton").addEventListener("click", async () => {
    const input = document.getElementById("textInput").value;
    if (!input) {
        alert("Por favor ingresa una noticia o URL.");
        return;
    }

    const isURL = input.startsWith("http");
    const requestData = isURL ? { url: input } : { text: input };

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();
        if (data.error) {
            document.getElementById("result").textContent = "Error: " + data.error;
        } else {
            document.getElementById("result").textContent = "Categoría: " + data.category;
        }
    } catch (error) {
        document.getElementById("result").textContent = "Error en la petición.";
    }
});
