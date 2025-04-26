document.addEventListener("DOMContentLoaded", function() {
  const sendButton = document.getElementById("sendButton");
  const messageInput = document.getElementById("messageInput");
  const fileInput = document.getElementById("fileInput");
  const fileButton = document.getElementById("fileButton");
  const messagesContainer = document.querySelector(".messages-container");

  function sendMessage(text, file) {
    if (!text && !file) return;

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "user");

    if (text) {
      messageDiv.textContent = text;
    }

    if (file) {
      messageDiv.textContent = "Arquivo enviado: " + file.name;
    }

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollIntoView({ block: "end", behavior: "smooth" });

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
});

