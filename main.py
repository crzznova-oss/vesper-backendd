<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VESPER // Conversational AI</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --astra-cyan: #00f0ff;
            --astra-glow: rgba(0, 240, 255, 0.25);
            --bg-dark: #030407;
            --panel-bg: rgba(10, 14, 23, 0.7);
            --border-light: rgba(255, 255, 255, 0.08);
            --user-msg: rgba(0, 240, 255, 0.1);
            --ai-msg: rgba(255, 255, 255, 0.03);
            --text-main: #f0f4f8;
            --text-muted: #627284;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Space Grotesk', sans-serif;
        }

        body {
            height: 100vh;
            width: 100vw;
            background-color: var(--bg-dark);
            color: var(--text-main);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 16px;
        }

        .nebula {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(0, 240, 255, 0.06) 0%, rgba(112, 0, 255, 0.04) 40%, transparent 70%);
            filter: blur(60px);
            z-index: 0;
            pointer-events: none;
        }

        /* Top Header */
        .top-nav {
            width: 100%;
            max-width: 800px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 10;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-light);
        }

        .brand {
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 2px;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .brand-dot {
            width: 8px;
            height: 8px;
            background: var(--astra-cyan);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--astra-cyan);
        }

        .status-pill {
            font-size: 11px;
            color: var(--astra-cyan);
            background: rgba(0, 240, 255, 0.1);
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid rgba(0, 240, 255, 0.2);
        }

        /* Chat Stream Area */
        .chat-container {
            width: 100%;
            max-width: 800px;
            flex: 1;
            overflow-y: auto;
            z-index: 10;
            margin: 16px 0;
            display: flex;
            flex-direction: column;
            gap: 14px;
            padding-right: 6px;
        }

        .chat-bubble {
            max-width: 85%;
            padding: 14px 18px;
            border-radius: 16px;
            font-size: 14px;
            line-height: 1.6;
            backdrop-filter: blur(15px);
            border: 1px solid var(--border-light);
            word-wrap: break-word;
        }

        .chat-bubble.user {
            align-self: flex-end;
            background: var(--user-msg);
            border-color: rgba(0, 240, 255, 0.3);
            border-bottom-right-radius: 4px;
        }

        .chat-bubble.assistant {
            align-self: flex-start;
            background: var(--ai-msg);
            border-bottom-left-radius: 4px;
        }

        .chat-bubble code {
            font-family: 'JetBrains Mono', monospace;
            background: rgba(0, 240, 255, 0.1);
            color: var(--astra-cyan);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 12px;
        }

        .chat-bubble pre {
            background: #000;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid var(--border-light);
            overflow-x: auto;
            margin: 8px 0;
        }

        /* Floating Command Bar */
        .command-dock {
            width: 100%;
            max-width: 800px;
            background: var(--panel-bg);
            border: 1px solid var(--border-light);
            backdrop-filter: blur(25px);
            border-radius: 30px;
            padding: 8px 12px 8px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            z-index: 10;
        }

        .command-input {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: #fff;
            font-size: 14px;
        }

        .send-btn {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--astra-cyan);
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
        }

        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px var(--astra-cyan);
        }

        .send-btn svg {
            width: 18px;
            height: 18px;
            fill: #000;
        }
    </style>
</head>
<body>

    <div class="nebula"></div>

    <div class="top-nav">
        <div class="brand">
            <div class="brand-dot"></div>
            <span>VESPER CHAT</span>
        </div>
        <div class="status-pill">● Online</div>
    </div>

    <!-- Chat History Stream -->
    <div class="chat-container" id="chatContainer">
        <div class="chat-bubble assistant">
            Hello! I am Vesper. What are we building or discussing today?
        </div>
    </div>

    <!-- Message Input Dock -->
    <div class="command-dock">
        <input type="text" class="command-input" id="messageInput" placeholder="Message Vesper..." onkeydown="handleKey(event)">
        <button class="send-btn" id="sendBtn" onclick="sendMessage()">
            <svg viewBox="0 0 24 24">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path>
            </svg>
        </button>
    </div>

    <script>
        // Store ongoing message thread
        const conversationHistory = [];

        function handleKey(event) {
            if (event.key === 'Enter') sendMessage();
        }

        async function sendMessage() {
            const input = document.getElementById("messageInput");
            const text = input.value.trim();
            const chatContainer = document.getElementById("chatContainer");
            const sendBtn = document.getElementById("sendBtn");

            if (!text) return;

            // 1. Render User Message
            appendMessage("user", text);
            conversationHistory.push({ role: "user", content: text });
            input.value = "";

            // 2. Render Loading State
            const loadingBubble = appendMessage("assistant", "<em>Vesper is thinking...</em>");
            sendBtn.disabled = true;

            try {
                // 3. Post Chat History to FastAPI Backend
                const response = await fetch('https://vesper-backendd.onrender.com/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ messages: conversationHistory })
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    loadingBubble.innerHTML = marked.parse(data.reply);
                    conversationHistory.push({ role: "assistant", content: data.reply });
                } else {
                    loadingBubble.innerHTML = "<span style='color:#ff4d4d;'>Error: Could not process request.</span>";
                }
            } catch (error) {
                loadingBubble.innerHTML = "<span style='color:#ff4d4d;'>Network Error: Unable to connect to server.</span>";
            } finally {
                sendBtn.disabled = false;
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }

        function appendMessage(role, content) {
            const chatContainer = document.getElementById("chatContainer");
            const bubble = document.createElement("div");
            bubble.className = `chat-bubble ${role}`;
            bubble.innerHTML = role === "user" ? content : marked.parse(content);
            chatContainer.appendChild(bubble);
            chatContainer.scrollTop = chatContainer.scrollHeight;
            return bubble;
        }
    </script>
</body>
</html>
