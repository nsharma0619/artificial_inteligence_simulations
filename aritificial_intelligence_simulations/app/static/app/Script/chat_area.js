const chatWindow = document.querySelector(".chat-window");
const chatArea = document.querySelector(".chat-area");
const chatMessage = document.querySelector(".chat-type input");
const sendBtn = document.querySelector(".chat-type button");
const botBtn = document.querySelector(".demo.bottomright");
const closeBtn = document.querySelector(".chat-window > button");

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
	newChatMsg.innerText = chatMessage.value;

	let newAvatar = document.createElement("img");
	newAvatar.src =
		"https://images.freeimages.com/images/small-previews/e71/frog-1371919.jpg";

	let newChat = document.createElement("div");
	newChat.classList.add("msg", "rev");

	newChat.appendChild(newAvatar);
	newChat.appendChild(newChatMsg);

	chatArea.appendChild(newChat);

	let response = await fetch("http://127.0.0.1:8000/nsharma/chat/", {
		method: "POST",
		headers: {
			Accept: "application/json",
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			query: chatMessage.value,
		}),
	})
		.then((res) => res.json())
		.catch(() => console.log("Error has occured"));

	let newResMsg = document.createElement("p");
	newResMsg.innerText = response.reply;

	let newResAvatar = document.createElement("img");
	newResAvatar.src =
		"https://images.freeimages.com/images/small-previews/e71/frog-1371919.jpg";

	let newResChat = document.createElement("div");
	newResChat.classList.add("msg");

	newResChat.appendChild(newResAvatar);
	newResChat.appendChild(newResChatMsg);

	chatArea.appendChild(newResChat);

	chatMessage.value = "";
});
