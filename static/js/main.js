(function () {
    'use strict';

    /* Mobile sidebar toggle */
    var menuToggle = document.getElementById('menu-toggle');
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('sidebar-overlay');

    function openSidebar() {
        if (!sidebar) return;
        sidebar.classList.add('is-open');
        if (overlay) overlay.classList.add('is-visible');
        document.body.style.overflow = 'hidden';
    }

    function closeSidebar() {
        if (!sidebar) return;
        sidebar.classList.remove('is-open');
        if (overlay) overlay.classList.remove('is-visible');
        document.body.style.overflow = '';
    }

    if (menuToggle) {
        menuToggle.addEventListener('click', function () {
            if (sidebar && sidebar.classList.contains('is-open')) {
                closeSidebar();
            } else {
                openSidebar();
            }
        });
    }

    if (overlay) {
        overlay.addEventListener('click', closeSidebar);
    }

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeSidebar();
    });

    /* Close sidebar on nav link click (mobile) */
    if (sidebar) {
        sidebar.querySelectorAll('.nav-link').forEach(function (link) {
            link.addEventListener('click', function () {
                if (window.innerWidth <= 768) closeSidebar();
            });
        });
    }

    /* Dismissible alerts */
    document.querySelectorAll('.alert').forEach(function (alert) {
        var closeBtn = alert.querySelector('.alert-close');
        if (!closeBtn) return;

        closeBtn.addEventListener('click', function () {
            alert.style.transition = 'opacity 200ms ease, transform 200ms ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-4px)';
            setTimeout(function () {
                alert.remove();
            }, 200);
        });
    });

    /* Auto-dismiss success alerts after 5s */
    document.querySelectorAll('.alert-success').forEach(function (alert) {
        setTimeout(function () {
            if (!alert.parentNode) return;
            alert.style.transition = 'opacity 300ms ease';
            alert.style.opacity = '0';
            setTimeout(function () {
                if (alert.parentNode) alert.remove();
            }, 300);
        }, 5000);
    });

    /* Confirm delete forms */
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('submit', function (e) {
            var message = el.getAttribute('data-confirm') || 'Are you sure?';
            if (!window.confirm(message)) {
                e.preventDefault();
            }
        });
    });
})();

// =========================
// Dark Mode
// =========================

const themeToggle =
    document.getElementById("theme-toggle");


// Apply saved theme when page loads

if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
}


// Toggle theme

if (themeToggle) {

    themeToggle.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {

            localStorage.setItem("theme", "dark");

        } else {

            localStorage.setItem("theme", "light");

        }

        if (typeof updateChartsColors === "function") {
            updateChartsColors();
        }

    });

}

document.addEventListener('DOMContentLoaded', function () {

    const chatbotToggle = document.getElementById('chatbotToggle');
    const chatbotWindow = document.getElementById('chatbotWindow');
    const chatbotClose = document.getElementById('chatbotClose');
    const chatbotForm = document.getElementById('chatbotForm');
    const chatbotInput = document.getElementById('chatbotInput');
    const chatbotMessages = document.getElementById('chatbotMessages');
    const chatbotSend = document.getElementById('chatbotSend');

    let conversationId = null;


    if (!chatbotToggle) return;


    /* =========================
       OPEN / CLOSE CHAT
    ========================= */

    chatbotToggle.addEventListener('click', async function () {

        chatbotWindow.classList.toggle('show');

        if (chatbotWindow.classList.contains('show')) {

            chatbotInput.focus();

            /*
             Create conversation only once
            */
            if (!conversationId) {

                try {

                    const response = await fetch(
                        '/chatbot/new/',
                        {
                            method: 'GET'
                        }
                    );

                    const url = new URL(response.url);

                    conversationId = url.searchParams.get(
                        'conversation'
                    );

                    console.log(
                        'Conversation ID:',
                        conversationId
                    );

                } catch (error) {

                    console.error(
                        'Conversation error:',
                        error
                    );

                }

            }

        }

    });


    chatbotClose.addEventListener('click', function () {

        chatbotWindow.classList.remove('show');

    });


    /* =========================
       SEND MESSAGE
    ========================= */

    chatbotForm.addEventListener('submit', async function (event) {

        event.preventDefault();

        const message = chatbotInput.value.trim();

        if (!message) return;


        /*
         If conversation doesn't exist yet
        */

        if (!conversationId) {

            try {

                const conversationResponse = await fetch(
                    '/chatbot/new/'
                );

                const url = new URL(
                    conversationResponse.url
                );

                conversationId = url.searchParams.get(
                    'conversation'
                );

            } catch (error) {

                console.error(error);

                return;

            }

        }


        /* =========================
           USER MESSAGE
        ========================= */

        const userMessage = document.createElement('div');

        userMessage.className = 'user-message';

        userMessage.innerHTML = `
            <div class="message-text"></div>
        `;

        userMessage.querySelector(
            '.message-text'
        ).textContent = message;

        chatbotMessages.appendChild(userMessage);


        chatbotInput.value = '';

        chatbotMessages.scrollTop =
            chatbotMessages.scrollHeight;


        /* =========================
           LOADING MESSAGE
        ========================= */

        const loadingMessage =
            document.createElement('div');

        loadingMessage.className =
            'bot-message chatbot-loading';

        loadingMessage.innerHTML = `
            <div class="message-avatar">AI</div>

            <div class="message-text">
                Thinking...
            </div>
        `;

        chatbotMessages.appendChild(
            loadingMessage
        );

        chatbotMessages.scrollTop =
            chatbotMessages.scrollHeight;

        chatbotSend.disabled = true;


        /* =========================
           SEND TO DJANGO
        ========================= */

        try {

            const csrfToken =
                document.querySelector(
                    '[name=csrfmiddlewaretoken]'
                ).value;


            const formData = new FormData();

            formData.append(
                'conversation_id',
                conversationId
            );

            formData.append(
                'message',
                message
            );


            const response = await fetch(
                '/chatbot/send/',
                {
                    method: 'POST',

                    headers: {
                        'X-CSRFToken': csrfToken
                    },

                    body: formData
                }
            );


            const data = await response.json();


            loadingMessage.remove();


            /* =========================
               SUCCESS
            ========================= */

            if (data.success) {

                const botMessage =
                    document.createElement('div');

                botMessage.className =
                    'bot-message';

                botMessage.innerHTML = `
                    <div class="message-avatar">
                        AI
                    </div>

                    <div class="message-text"></div>
                `;


                botMessage.querySelector(
                    '.message-text'
                ).textContent = data.response;


                chatbotMessages.appendChild(
                    botMessage
                );

            }


            /* =========================
               ERROR FROM DJANGO
            ========================= */

            else {

                console.error(
                    'Django Error:',
                    data.error
                );

                const errorMessage =
                    document.createElement('div');

                errorMessage.className =
                    'bot-message';

                errorMessage.innerHTML = `
                    <div class="message-avatar">
                        AI
                    </div>

                    <div class="message-text"></div>
                `;


                errorMessage.querySelector(
                    '.message-text'
                ).textContent =
                    data.error || 'Sorry, something went wrong.';


                chatbotMessages.appendChild(
                    errorMessage
                );

            }


        } catch (error) {

            console.error(
                'Chatbot Error:',
                error
            );

            loadingMessage.remove();


            const errorMessage =
                document.createElement('div');

            errorMessage.className =
                'bot-message';

            errorMessage.innerHTML = `
                <div class="message-avatar">
                    AI
                </div>

                <div class="message-text">
                    Sorry, I couldn't connect right now.
                </div>
            `;

            chatbotMessages.appendChild(
                errorMessage
            );

        }


        chatbotSend.disabled = false;

        chatbotMessages.scrollTop =
            chatbotMessages.scrollHeight;

    });

});