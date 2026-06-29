let websocket = $state({
  connection: null,
  connected: false,
  error: ""
})


export function connect() {
  console.log("Connecting")
  if (websocket.connected) return;
  websocket.connection = new WebSocket("ws://localhost:8000/ws");
  websocket.connection.onopen = () => { console.log("Connected"); websocket.connected = true; };
  websocket.connection.onmessage = async (e) => {
    const text = await e.data.text();
    const packet = JSON.parse(text); // Change these later on
    test(packet)
  }
  websocket.connection.onclose = () => websocket.connected = false;
}

export function disconnect() {
  websocket.connection?.close();
}

export function subscribe(events, exchange) {
  console.log('ws state:', websocket.connected, websocket.connection?.readyState);
  if (!websocket.connected) return;

  const packet = JSON.stringify({ method: "sub", events, exchange });

  console.log('sending:', packet)
  websocket.connection.send(new TextEncoder().encode(packet));
}

function test(packet) {
  console.log(packet)
}

export const websocketStore = {
  get connection() { return websocket.connection },
  get isConnected() { return websocket.connected },
  get error() { return websocket.error }
}
