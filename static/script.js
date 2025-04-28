document.addEventListener("DOMContentLoaded", function() {
  const sendButton = document.getElementById("sendButton");
  const messageInput = document.getElementById("messageInput");
  const fileInput = document.getElementById("fileInput");
  const fileButton = document.getElementById("fileButton");
  const messagesContainer = document.querySelector(".messages-container");
  const select = document.getElementById("models");
  const sumarized = document.getElementById("sumarized");
  const nResults = document.getElementById("n-results");

  fetch('/models', {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
    .then(function(response) {
      return response.json();
    })
    .then(function(json) {
      Object.keys(json.response).forEach((model) => {
        const option = document.createElement('option');

        option.value = model;
        option.textContent = json.response[model];

        if (model == 'multi-qa-MiniLM-L6-cos-v1') {
          option.selected = true;
        }

        select.appendChild(option);
      });
    });


  function makeMessage(messageDiv, json) {
    const data = json.response;

    messageDiv.innerHTML = "Currículos encontrados: <br /><br />";

    Object.keys(data).forEach((id) => {
      const div = document.createElement('div');

      div.className = "document-link"

      div.textContent = id + ": " + data[id].labels.join(", ");

      div.addEventListener('click', function() {
        openModal(data[id].desc);
      });

      messageDiv.appendChild(div);
    });
  }

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async function searchByText(text) {
    await sleep(500);

    const messageDiv = sendSystemMensage();

    fetch('/chat', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: select.value,
        sumarized: sumarized.value,
        message: text,
        n_results: nResults.value
      })
    })
      .then(function(response) {
        return response.json();
      })
      .then(function(json) {
        makeMessage(messageDiv, json)
      });
  }

  async function searchByFile(file) {
    await sleep(500);

    const messageDiv = sendSystemMensage();

    const formData = new FormData();

    formData.append('model', select.value);
    formData.append('sumarized', sumarized.value);
    formData.append('n_results', nResults.value);
    formData.append('file', file);

    fetch('/upload', {
      method: 'POST',
      body: formData
    })
      .then(function(response) {
        return response.json();
      })
      .then(function(json) {
        makeMessage(messageDiv, json)
      });
  }

  function addSpace() {
    const container = document.querySelector('.messages-container');

    const div = document.createElement('div');

    div.className = "space";
    div.innerHTML = "<br><br><br><br>"

    container.querySelectorAll('.space').forEach(spaceDiv => spaceDiv.remove());
    container.appendChild(div)
  }

  function sendSystemMensage() {
    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");

    messageDiv.textContent = "...";

    messagesContainer.appendChild(messageDiv);

    addSpace();

    return messageDiv;
  }

  function sendMessage(text, file) {
    if (!text && !file) return;
    addSpace();

    const container = document.querySelector('.messages-container');
    container.querySelectorAll('.space').forEach(spaceDiv => spaceDiv.remove());

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "user");

    if (text) {
      messageDiv.textContent = text;

      searchByText(text);
    }

    if (file) {
      messageDiv.textContent = "Arquivo enviado: " + file.name;

      searchByFile(file);
    }

    messagesContainer.appendChild(messageDiv);

    messageInput.value = "";
    fileInput.value = "";
  }

  sendButton.addEventListener("click", function() {
    sendMessage(messageInput.value.trim());
  });

  messageInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage(messageInput.value.trim());
    }
  });

  fileButton.addEventListener("click", function() {
    fileInput.click();
  });

  fileInput.addEventListener("change", function() {
    const file = fileInput.files[0];
    if (file) {
      sendMessage(null, file);
    }
  });

  function openModal(text) {
    const modal = document.getElementById("documentModal");
    const modalText = document.getElementById("modalText");

    modalText.textContent = text;
    modal.style.display = "block";
  }

  document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
      document.getElementById("documentModal").style.display = "none";
    }
  });

  window.addEventListener("click", function(event) {
    const modal = document.getElementById("documentModal");
    if (event.target == modal) {
      modal.style.display = "none";
    }
  });
});

