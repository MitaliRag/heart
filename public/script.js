const form =
    document.getElementById("predictionForm");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const resultText =
    document.getElementById("resultText");

const probability =
    document.getElementById("probability");


form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        loading.style.display = "block";
        result.style.display = "none";


        const data = {

            age: Number(
                document.getElementById("age").value
            ),

            sex: Number(
                document.getElementById("sex").value
            ),

            cp: Number(
                document.getElementById("cp").value
            ),

            trestbps: Number(
                document.getElementById("trestbps").value
            ),

            chol: Number(
                document.getElementById("chol").value
            ),

            fbs: Number(
                document.getElementById("fbs").value
            ),

            restecg: Number(
                document.getElementById("restecg").value
            ),

            thalach: Number(
                document.getElementById("thalach").value
            ),

            exang: Number(
                document.getElementById("exang").value
            ),

            oldpeak: Number(
                document.getElementById("oldpeak").value
            ),

            slope: Number(
                document.getElementById("slope").value
            ),

            ca: Number(
                document.getElementById("ca").value
            ),

            thal: Number(
                document.getElementById("thal").value
            )
        };


        try {

            const response =
                await fetch(
                    "http://127.0.0.1:8000/predict",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(data)
                    }
                );


            const output =
                await response.json();


            if (!output.success) {

                throw new Error(
                    output.error
                );

            }


            resultText.textContent =
                output.result;

            probability.textContent =
                output.probability + "%";


            result.style.display =
                "block";


        } catch (error) {

            alert(
                "Error: " +
                error.message
            );

        }


        loading.style.display =
            "none";

    }
);