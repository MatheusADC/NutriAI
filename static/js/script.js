document.getElementById("formRecomendacao").addEventListener("submit", async function(event) {
    event.preventDefault();

    const divBotaoRecomendacao = document.getElementById("divRecomendacao");
    const loading = document.getElementById("loading");
    loading.style.display = "block"; 

    if(loading.style.display == "block") {
        divBotaoRecomendacao.style.display = "none";
    }

    const formData = new FormData(this);
    const file = document.getElementById("pdfExame").files[0];
    const nome = document.getElementById("nome").value;
    const colesterolTotal = document.getElementById("colesterol_total").value;
    const glicose = document.getElementById("glicose").value;
    const t3 = document.getElementById("t3").value;
    const t4 = document.getElementById("t4").value;
    const tsh = document.getElementById("tsh").value;
    const triglicerideos = document.getElementById("triglicerideos").value;

    if (!file && !colesterolTotal && !glicose && !t3 && !t4 && !tsh && !triglicerideos) {
        alert("Por favor, preencha os campos ou anexe um PDF.");
        loading.style.display = "none"; 
        return;
    }

    if (file && !nome) {
        alert("O campo 'Nome' é obrigatório quando um PDF é anexado.");
        loading.style.display = "none"; 
        return;
    }

    formData.append("nome", nome);

    if (file) {
        formData.append("pdfExame", file);
    } else {
        formData.append("colesterol_total", colesterolTotal);
        formData.append("glicose", glicose);
        formData.append("t3", t3);
        formData.append("t4", t4);
        formData.append("tsh", tsh);
        formData.append("triglicerideos", triglicerideos);
    }

    try {
        const response = await fetch("/upload_pdf", {
            method: "POST",
            body: formData
        });

        loading.style.display = "none"; 

        if (response.ok) {
            const htmlContent = await response.text();
            document.open();
            document.write(htmlContent);
            document.close();
        } else {
            console.log("Falha no envio do formulário.");
        }
    } catch (error) {
        console.error("Erro ao enviar o formulário:", error);
        loading.style.display = "none"; 
    }
});
