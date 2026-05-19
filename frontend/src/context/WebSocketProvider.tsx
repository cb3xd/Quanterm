import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ChangeEvent,
} from "react";

const WebSocketContext = createContext();

export function WebSocketProvider({ children }) {
  const [ws, setWs] = useState<Websocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [listeners, setListeners] = useState<Record<string, Function[]>>({});

  const subscribe = (eventId: string, callback: Function) => {
    //register listener for eventId
  };

  const sendMessage = (message: object) => {
    //send to server
  };

  useEffect(() => {
    const newWs = new WebSocket("ws://localhost:8000/ws/");
    newWs.onopen = () => setIsConnected(true);
    newWs.onmessage = (event) => {
      const json = new TextDecoder().decode(event.data);
      const packet = JSON.parse(json);
    };

    newWs.onclose = () => setIsConnected(false);
    setWs(newWs);
    return () => newWs.close();
  }, []);

  const value = useMemo(
    () => ({
      ws,
      isConnected,
      subscribe,
      sendMessage,
    }),
    [ws, isConnected, subscribe, sendMessage],
  );
  return (
    <WebSocketContext.Provider value={value}>
      {children}
    </WebSocketContext.Provider>
  );
}

export function useWebSocket() {
  return useContext(WebSocketContext);
}
