
const form = document.getElementById("emailForm");
const sendButton = document.getElementById("sendButton");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    document.getElementById("placeholder").classList.add("hidden");
    document.getElementById("result").classList.add("hidden");
    document.getElementById("error").classList.add("hidden");
    document.getElementById("loading").classList.remove("hidden");

    sendButton.disabled = true;

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                customer_name: document.getElementById("customer_name").value,
                subject: document.getElementById("subject").value,
                email: document.getElementById("email").value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to analyze the email.");
        }

        document.getElementById("intent").textContent = data.intent;
        document.getElementById("reply").textContent = data.reply;
        document.getElementById("summary").textContent = data.summary;
        document.getElementById("result").classList.remove("hidden");
    } catch (error) {
        document.getElementById("error").textContent = error.message;
        document.getElementById("error").classList.remove("hidden");
    } finally {
        document.getElementById("loading").classList.add("hidden");
        sendButton.disabled = false;
    }
});

document.getElementById("toneButton").addEventListener("click", async function () {
    const message = document.getElementById("message");
    message.textContent = "Improving tone...";

    try {
        const response = await fetch("/api/tone", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                reply: document.getElementById("reply").textContent,
                tone: document.getElementById("tone").value
            })
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error || "Tone improvement failed.");

        document.getElementById("reply").textContent = data.reply;
        message.textContent = "Tone updated successfully.";
    } catch (error) {
        message.textContent = error.message;
    }
});

document.getElementById("saveButton").addEventListener("click", async function () {
    const message = document.getElementById("message");
    message.textContent = "Saving reply...";

    try {
        const response = await fetch("/api/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                customer_name: document.getElementById("customer_name").value,
                subject: document.getElementById("subject").value,
                email: document.getElementById("email").value,
                intent: document.getElementById("intent").textContent,
                reply: document.getElementById("reply").textContent,
                summary: document.getElementById("summary").textContent
            })
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error || "Saving failed.");

        message.textContent = data.message;
    } catch (error) {
        message.textContent = error.message;
    }
});
