document.getElementById("sendButton").addEventListener("click", async () => {
    const text = document.getElementById("newsInput").value;
    const resultElement = document.getElementById("result");

    if (!text.trim()) {
        resultElement.textContent = "Por favor, introduce un texto.";
        return;
    }

    resultElement.textContent = "Clasificando...";
    
    try {
        const response = await fetch("http://localhost:5000/classify", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        resultElement.textContent = `Categoría: ${data.class}`;
    } catch (error) {
        resultElement.textContent = "Error en la clasificación.";
    }
});
