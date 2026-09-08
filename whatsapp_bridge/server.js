const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');
const express = require('express');
const qrcode = require('qrcode-terminal');

const app = express();
app.use(express.json());

let sock;

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info_baileys');
    
    sock = makeWASocket({
        auth: state,
        printQRInTerminal: false
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;
        
        if (qr) {
            console.log('\n--- SCAN THIS QR CODE WITH WHATSAPP ---');
            qrcode.generate(qr, { small: true });
        }

        if (connection === 'close') {
            const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log('Connection closed, reconnecting:', shouldReconnect);
            if (shouldReconnect) connectToWhatsApp();
        } else if (connection === 'open') {
            console.log('✅ ASTRA WhatsApp Bridge Connected Successfully!');
        }
    });

    // Inbound Message Handler
    sock.ev.on('messages.upsert', async ({ messages, type }) => {
        if (type === 'notify') {
            for (const msg of messages) {
                // Group messages ko ignore karke sirf Direct Messages handle karne ke liye check
                const isGroup = msg.key.remoteJid.endsWith('@g.us');
                
                if (!msg.key.fromMe && msg.message && !isGroup) {
                    const incomingText = msg.message.conversation || msg.message.extendedTextMessage?.text;
                    const senderNumber = msg.key.remoteJid;

                    if (incomingText) {
                        console.log(`📩 Direct Message from ${senderNumber}: ${incomingText}`);

                        // Forward to n8n Webhook
                        try {
                            // Localhost use karein kyunki Node host machine par hai aur n8n Docker port 5678 par mapped hai
                            const response = await fetch('http://localhost:5678/webhook-test/astra-input', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    sender: senderNumber,
                                    message: incomingText
                                })
                            });

                            if (!response.ok) {
                                console.error(`⚠️ n8n Webhook HTTP Error! Status: ${response.status}`);
                            } else {
                                console.log('🚀 Message successfully sent to n8n!');
                            }
                        } catch (err) {
                            console.error('⚠️ Could not send to n8n webhook:', err.message);
                        }
                    }
                }
            }
        }
    });
}

// Endpoint for n8n to send outgoing messages
app.post('/send-message', async (req, res) => {
    try {
        const { number, message } = req.body;
        if (!number || !message) {
            return res.status(400).json({ status: 'error', error: 'Number and message are required' });
        }

        const formattedNumber = `${number.replace(/[^0-9]/g, '')}@s.whatsapp.net`;
        
        await sock.sendMessage(formattedNumber, { text: message });
        res.status(200).json({ status: 'success', message: 'Message sent!' });
    } catch (error) {
        console.error('Error sending message:', error);
        res.status(500).json({ status: 'error', error: error.message });
    }
});

app.listen(3000, () => {
    console.log('🚀 ASTRA Bridge running on http://localhost:3000');
    connectToWhatsApp();
});