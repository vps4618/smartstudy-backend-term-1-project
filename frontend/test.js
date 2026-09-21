// Connect securely via wss:// and pass the key in the URL
const apiKey = "gizmo-secure-key-2026";
const ws = new WebSocket(`wss://smartstudy-backend-psi.vercel.app/api/ws?api_key=${apiKey}`);

ws.onopen = () => {
    console.log("Secure WebSocket connected.");
};

ws.onmessage = (event) => {
    // Update the UI dynamically when occupancy changes
    const liveData = JSON.parse(event.data);
    console.log("New Occupancy:", liveData.new_occupancy);
};

ws.onclose = (event) => {
    if (event.code === 1008) {
        console.error("Connection rejected: Invalid API Key");
    }
};