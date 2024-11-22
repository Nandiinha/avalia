var btnLogin = document.querySelector("#redirect-login");
var btnRegister = document.querySelector("#redirect-register");
var body = document.querySelector("body");

if(btnLogin){
    btnLogin.addEventListener("click", function(){
        body.className = "login-js";
    });    
}

if(btnRegister){
    btnRegister.addEventListener("click", function(){
        body.className = "register-js";
    });
}

async function startCorrection() {
    const loader = createLoader();
    loader.show();
  
    try {
      const form = document.getElementById("answerForm");
      const fileInput = document.getElementById("studentAnswer");
  
      if (!fileInput.value) {
        showMessage({
          message: 'Por favor, selecione um arquivo antes de continuar.',
          type: 'toast',
          severity: 'error',
          containerId: 'correctionModal_AlertPlaceHolder',
        }); // Exibe como Alert
        return;
      }
  
      const formData = new FormData(form);
  
      // Realiza a requisição utilizando `await`
      const response = await fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
      });
  
      // Verifica se a resposta foi bem-sucedida
      if (!response.ok) {
        throw new Error("Erro ao extrair texto. Verifique o arquivo enviado.");
      }
  
      const data = await response.json(); // Aguarda a conversão da resposta em JSON
      console.log("Resposta do servidor:", data);
  
      // Manipula os dados retornados
      document.getElementById("score").value = data.score;
      document.getElementById("feedback").textContent = data.feedback || "Sem feedback disponível.";
      document.getElementById("extract_value").textContent = data.extract_value;
  
      document.getElementById("corrigirButton").classList.add("display-tags");
      document.getElementById("salvarButton").classList.remove("display-tags");
      document.getElementById("scorediv").classList.remove("display-tags");
      document.getElementById("feedbackdiv").classList.remove("display-tags");
      document.getElementById("extract_valuediv").classList.remove("display-tags");
      document.getElementById("studentAnswerdiv").classList.add("display-tags");
  
      console.log("Correção iniciada, pontuação:", data.score);
    } catch (error) {
      console.error("Erro na correção:", error.message);
      showMessage({
        message: error.message,
        type: 'toast',
        severity: 'error',
        containerId: 'correctionModal_AlertPlaceHolder',
      }); // Exibe como Toast
    } finally {
      loader.hide(); // Esconde o loader independentemente do sucesso ou erro
    }
}  

function saveCorrection(activityId) {

    const form = document.getElementById("answerForm");
    const formData = new FormData(form);
    formData.append("id_student", parseInt(document.getElementById("studentName").value,10))

    fetch("/correction/create_answer/"+activityId+"/", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    }).then(data => {
        if(data.ok){
            alert("Form salvo com sucesso")
            window.location.reload()
        }else
        {
            
        alert("Form salvo com erros!")
        }
    }).catch(()=>{
        alert(err.message)
    })
}


