let websocket = $state({
  connection: null,
  connected: false,
  error: ""
})

let packetBuffer = $state({
  streams: {},
})

let exchangeRegistry = $derived(Array.from(new Set(Object.keys(packetBuffer.streams).map(k => k.split('.')[0]))));

export function connect() {
  if (websocket.connected) return;
  websocket.connection = new WebSocket("ws://localhost:8000/ws");
  websocket.connection.onopen = () => { websocket.connected = true; };
  websocket.connection.onmessage = async (e) => {
    const text = await e.data.text();
    const packet = JSON.parse(text); // Change these later on

    packetBuffer.streams[packet.event_id] = packet;
  }
  websocket.connection.onclose = () => websocket.connected = false;
}

export function disconnect() {
  websocket.connection?.close();
}

export function subscribe(events, exchange) {
  if (!websocket.connected) return;

  const packet = JSON.stringify({ method: "sub", events, exchange });

  websocket.connection.send(new TextEncoder().encode(packet));
}


export const websocketStore = {
  get connection() { return websocket.connection },
  get isConnected() { return websocket.connected },
  get error() { return websocket.error },
}
export const streamsStore = {
  get streams() { return packetBuffer.streams },
}
export const exchangesStore = {
  get exchanges() { return exchangeRegistry }
}
