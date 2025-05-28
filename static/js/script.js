document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const chatSection = document.getElementById('chat-section');
    const sobreSection = document.getElementById('sobre-section');
    const duvidasSection = document.getElementById('duvidas-section');
    const cidadesSection = document.getElementById('cidades-section');
    const menuButtons = document.querySelectorAll('.menu-btn');
    const livreBtn = document.getElementById('livre-btn');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const quickQuestions = document.querySelectorAll('.quick-question');
    
    // Menu navigation
    menuButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            menuButtons.forEach(btn => btn.classList.remove('active', 'btn-light'));
            menuButtons.forEach(btn => btn.classList.add('btn-outline-light'));
            
            // Add active class to clicked button
            this.classList.remove('btn-outline-light');
            this.classList.add('active', 'btn-light');
            
            // Hide all sections
            document.querySelectorAll('.section').forEach(section => {
                section.classList.add('d-none');
            });
            
            // Show selected section
            const sectionId = this.getAttribute('data-section') + '-section';
            document.getElementById(sectionId).classList.remove('d-none');
        });
    });
    
    // Toggle free mode
    let livreMode = false;
    livreBtn.addEventListener('click', function() {
        livreMode = !livreMode;
        if (livreMode) {
            this.classList.remove('btn-outline-light');
            this.classList.add('btn-success');
            addBotMessage("Modo livre ativado! Você pode perguntar qualquer coisa sobre programação.");
        } else {
            this.classList.remove('btn-success');
            this.classList.add('btn-outline-light');
            addBotMessage("Modo livre desativado. Voltando ao modo Jovem Programador.");
        }
    });
    
    // Send message
    async function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
        addUserMessage(message);
        userInput.value = '';
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            addBotMessage(data.response);
        } catch (error) {
            addBotMessage("Ops, tive um problema para responder. Tente novamente!");
            console.error('Error:', error);
        }
    }
}

async function loadData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        
        // Atualize as seções com os dados reais
        document.getElementById('sobre-content').textContent = data.sobre.split('\n\n')[0];
        document.getElementById('cidades-content').textContent = data.cidades;
        
        // Preencha o accordion de dúvidas
        const accordion = document.getElementById('duvidas-accordion');
        Object.entries(data.duvidas).forEach(([pergunta, resposta], i) => {
            const item = document.createElement('div');
            item.className = 'accordion-item';
            item.innerHTML = `
                <h2 class="accordion-header" id="heading${i}">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                        data-bs-target="#collapse${i}" aria-expanded="false" aria-controls="collapse${i}">
                        ${pergunta}
                    </button>
                </h2>
                <div id="collapse${i}" class="accordion-collapse collapse" aria-labelledby="heading${i}" 
                    data-bs-parent="#duvidas-accordion">
                    <div class="accordion-body">
                        ${resposta}
                    </div>
                </div>
            `;
            accordion.appendChild(item);
        });
    } catch (error) {
        console.error('Error loading data:', error);
    }
}
    
    // Quick questions
    quickQuestions.forEach(button => {
        button.addEventListener('click', function() {
            userInput.value = this.textContent;
            sendMessage();
        });
    });
    
    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
    
    // Helper functions
    function addUserMessage(text) {
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user';
        messageDiv.innerHTML = `
            <div class="message-content">${text}</div>
            <div class="message-time">${timeString}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function addBotMessage(text) {
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';
        messageDiv.innerHTML = `
            <div class="message-content">${text}</div>
            <div class="message-time">${timeString}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Load data from backend (simulated)
    function loadData() {
        // Simulate loading sobre
        setTimeout(() => {
            document.getElementById('sobre-content').textContent = "O JOVEM PROGRAMADOR é um PROGRAMA de capacitação tecnológica para formação de pessoas, a partir de 16 anos...";
        }, 500);
        
        // Simulate loading dúvidas
        setTimeout(() => {
            const accordion = document.getElementById('duvidas-accordion');
            const questions = [
                { pergunta: "Quem pode participar?", resposta: "Pessoas a partir de 16 anos..." },
                { pergunta: "O programa tem algum custo?", resposta: "O Jovem Programador é gratuito para pessoas com renda familiar..." },
                { pergunta: "Quando começam as aulas?", resposta: "As aulas estão previstas para começar na segunda quinzena de março..." }
            ];
            
            questions.forEach((q, i) => {
                const item = document.createElement('div');
                item.className = 'accordion-item';
                item.innerHTML = `
                    <h2 class="accordion-header" id="heading${i}">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                            data-bs-target="#collapse${i}" aria-expanded="false" aria-controls="collapse${i}">
                            ${q.pergunta}
                        </button>
                    </h2>
                    <div id="collapse${i}" class="accordion-collapse collapse" aria-labelledby="heading${i}" 
                        data-bs-parent="#duvidas-accordion">
                        <div class="accordion-body">
                            ${q.resposta}
                        </div>
                    </div>
                `;
                accordion.appendChild(item);
            });
        }, 800);
        
        // Simulate loading cidades
        setTimeout(() => {
            document.getElementById('cidades-content').textContent = "Araranguá, Blumenau, Biguaçu, Brusque, Caçador...";
        }, 700);
    }
    
    // Initialize
    loadData();
});