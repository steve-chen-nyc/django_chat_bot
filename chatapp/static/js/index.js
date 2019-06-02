const ChatHandler = () => {
    const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/`);

    const botTemplate = (message) => `<li class="message bot"><span>ChatBot: </span>${message}</li>`;

    const userTemplate = (message, name) => `<li class="message user"><span>${name}: </span>${message}</li>`;

    const handleSocketEvents = () => {
        chatSocket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            const message = data['message'];
            const isBot = data['bot'];
            const name = data['userName'];
            const chatContainer = document.querySelector(".chat-list");

            const template = isBot ? botTemplate(message) : userTemplate(message, name);

            chatContainer.innerHTML += template;
        };

        chatSocket.onclose = (e) => {
            console.error('Chat socket closed unexpectedly');
        };
    }

    const handleSubmit = () => {
        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = (e) => {
            if (e.keyCode === 13) {
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = (e) => {
            let messageInputDom = document.querySelector('#chat-message-input');
            let message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));

            messageInputDom.value = '';
        };
    }

    const init = () => {
        handleSocketEvents();
        handleSubmit();
    }

    return {
        init: init
    };
};

const chatHandler = ChatHandler();

chatHandler.init();
