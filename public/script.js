
const form = document.getElementById("predictionForm");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const resultText = document.getElementById("resultText");
const probability = document.getElementById("probability");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    loading.style.display = "block";
    result.style.display = "none";

    const data = {
        age: Number(document.getElementById("age").value),
        sex: Number(document.getElementById("sex").value),
        cp: Number(document.getElementById("cp").value),
        trestbps: Number(document.getElementById("trestbps").value),
        chol: Number(document.getElementById("chol").value),
        fbs: Number(document.getElementById("fbs").value),
        restecg: Number(document.getElementById("restecg").value),
        thalach: Number(document.getElementById("thalach").value),
        exang: Number(document.getElementById("exang").value),
        oldpeak: Number(document.getElementById("oldpeak").value),
        slope: Number(document.getElementById("slope").value),
        ca: Number(document.getElementById("ca").value),
        thal: Number(document.getElementById("thal").value)
    };

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const output = await response.json();

        if (!response.ok) {
            throw new Error(
                output.detail ||
                output.error ||
                `Server error: ${response.status}`
            );
        }

        if (output.success !== true) {
            throw new Error(output.error || "Prediction failed.");
        }

        resultText.textContent = output.result;

        const probabilityValue =
            output.probability ?? output.risk_probability;

        if (probabilityValue !== null &&
            probabilityValue !== undefined) {
            const numericValue = Number(probabilityValue);
            const percent = numericValue <= 1
                ? numericValue * 100
                : numericValue;

            probability.textContent = percent.toFixed(2) + "%";
        } else {
            probability.textContent = "Probability unavailable";
        }

        result.style.display = "block";

    } catch (error) {
        console.error("Prediction error:", error);
        alert("Prediction Error: " + error.message);
    } finally {
        loading.style.display = "none";
    }
});
