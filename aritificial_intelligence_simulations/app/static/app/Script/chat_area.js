const chatWindow = document.querySelector(".chat-window");
const chatArea = document.querySelector(".chat-area");
const chatMessage = document.querySelector(".chat-type input");
const sendBtn = document.querySelector(".chat-type button");
const botBtn = document.querySelector(".demo.bottomright");
const closeBtn = document.querySelector(".close-btn");

botBtn.addEventListener("click", () => {
	botBtn.classList.add("disappear");
	chatWindow.classList.remove("disappear");
});

closeBtn.addEventListener("click", () => {
	botBtn.classList.remove("disappear");
	chatWindow.classList.add("disappear");
});

sendBtn.addEventListener("click", async () => {
	let newChatMsg = document.createElement("p");
	let msg = chatMessage.value;
	newChatMsg.innerText = msg;
	if(msg!=""){
	let newAvatar = document.createElement("img");
	newAvatar.src =
		"https://images.freeimages.com/images/small-previews/e71/frog-1371919.jpg";

	let newChat = document.createElement("div");
	newChat.classList.add("msg", "rev");

	newChat.appendChild(newAvatar);
	newChat.appendChild(newChatMsg);

	chatArea.appendChild(newChat);
	chatMessage.value = "";
	chatArea.scrollTop = chatArea.scrollHeight;
	let response = await fetch("http://127.0.0.1:8000/chatbot/NeerajSingh/chat/", {
		method: "POST",
		headers: {
			Accept: "application/json",
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			query: msg,
		}),
	})
		.then((res) => res.json())
		.catch(() => console.log("Error has occured"));
	console.log(response.reply);
	let newResMsg = document.createElement("p");
	newResMsg.innerText = response.reply;

	let newResAvatar = document.createElement("img");
	newResAvatar.src =
		"https://images.freeimages.com/images/small-previews/e71/frog-1371919.jpg";

	let newResChat = document.createElement("div");
	newResChat.classList.add("msg");

	newResChat.appendChild(newResAvatar);
	newResChat.appendChild(newResMsg);

	chatArea.appendChild(newResChat);
	}
	chatArea.scrollTop = chatArea.scrollHeight;
});

