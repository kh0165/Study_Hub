document.addEventListener("DOMContentLoaded", () => {

    const form =
        document.getElementById("chatbot-form");

    if (!form) {
        return;
    }


    const input =
        document.getElementById("chatbot-input");


    const messagesContainer =
        document.getElementById(
            "chatbot-messages"
        );


    const sendButton =
        document.getElementById(
            "chatbot-send-btn"
        );


    const conversationId =
        document.getElementById(
            "conversation-id"
        );


    const sendUrl =
        form.dataset.sendUrl;


    function getCSRFToken() {

        const csrfInput =
            form.querySelector(
                'input[name="csrfmiddlewaretoken"]'
            );

        return csrfInput
            ? csrfInput.value
            : "";
    }


    function scrollToBottom() {

        if (!messagesContainer) {
            return;
        }

        messagesContainer.scrollTop =
            messagesContainer.scrollHeight;
    }


    function createMessageElement(
        role,
        content
    ) {

        const wrapper =
            document.createElement("div");

        wrapper.className =
            role === "user"
                ? "chatbot-message chatbot-message-user"
                : "chatbot-message chatbot-message-ai";


        const avatar =
            document.createElement("div");

        avatar.className =
            "chatbot-avatar";

        avatar.textContent =
            role === "user"
                ? "You"
                : "AI";


        const contentWrapper =
            document.createElement("div");

        contentWrapper.className =
            "chatbot-message-content";


        const roleElement =
            document.createElement("div");

        roleElement.className =
            "chatbot-message-role";

        roleElement.textContent =
            role === "user"
                ? "You"
                : "StudyHub AI";


        const text =
            document.createElement("div");

        text.className =
            "chatbot-message-text";

        text.textContent =
            content;


        contentWrapper.appendChild(
            roleElement
        );

        contentWrapper.appendChild(
            text
        );

        wrapper.appendChild(
            avatar
        );

        wrapper.appendChild(
            contentWrapper
        );


        return wrapper;
    }


    function createLoadingMessage() {

        const wrapper =
            createMessageElement(
                "assistant",
                "Thinking..."
            );

        wrapper.id =
            "chatbot-loading";

        return wrapper;
    }


    async function sendMessage(message) {

        if (!message.trim()) {
            return;
        }


        if (!conversationId.value) {
            return;
        }


        sendButton.disabled = true;

        input.disabled = true;


        const welcome =
            document.querySelector(
                ".chatbot-welcome"
            );


        if (welcome) {
            welcome.remove();
        }


        const userMessage =
            createMessageElement(
                "user",
                message
            );


        messagesContainer.appendChild(
            userMessage
        );


        input.value = "";

        scrollToBottom();


        const loadingMessage =
            createLoadingMessage();


        messagesContainer.appendChild(
            loadingMessage
        );


        scrollToBottom();


        const formData =
            new FormData();


        formData.append(
            "message",
            message
        );


        formData.append(
            "conversation_id",
            conversationId.value
        );


        formData.append(
            "csrfmiddlewaretoken",
            getCSRFToken()
        );


        try {

            const response =
                await fetch(
                    sendUrl,
                    {
                        method: "POST",

                        body: formData,

                        headers: {
                            "X-Requested-With":
                                "XMLHttpRequest"
                        }
                    }
                );


            const data =
                await response.json();


            const loading =
                document.getElementById(
                    "chatbot-loading"
                );


            if (loading) {
                loading.remove();
            }


            if (
                !response.ok ||
                !data.success
            ) {

                const errorMessage =
                    createMessageElement(
                        "assistant",
                        data.error ||
                        "Something went wrong."
                    );


                messagesContainer.appendChild(
                    errorMessage
                );

            } else {

                const aiMessage =
                    createMessageElement(
                        "assistant",
                        data.response
                    );


                messagesContainer.appendChild(
                    aiMessage
                );
            }


            scrollToBottom();

        } catch (error) {

            const loading =
                document.getElementById(
                    "chatbot-loading"
                );


            if (loading) {
                loading.remove();
            }


            const errorMessage =
                createMessageElement(
                    "assistant",
                    "Unable to connect to the AI assistant."
                );


            messagesContainer.appendChild(
                errorMessage
            );


            console.error(error);

        } finally {

            sendButton.disabled = false;

            input.disabled = false;

            input.focus();
        }
    }


    form.addEventListener(
        "submit",
        (event) => {

            event.preventDefault();

            sendMessage(
                input.value
            );
        }
    );


    input.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                form.requestSubmit();
            }
        }
    );


    document
        .querySelectorAll(
            ".chatbot-suggestion"
        )
        .forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        const message =
                            button.dataset.message;

                        sendMessage(
                            message
                        );
                    }
                );
            }
        );


    scrollToBottom();
});