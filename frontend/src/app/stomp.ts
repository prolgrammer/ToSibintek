import { Middleware } from '@reduxjs/toolkit';
import { Client } from '@stomp/stompjs';
import { RootState } from '../app/store';
import { setClient, setConnectionStatus } from '@entities/webSocketSlice';
import { jwtDecode } from 'jwt-decode';
import Cookies from "js-cookie"

type jwtPayload = {
  id: string
}
// eslint-disable-next-line @typescript-eslint/no-empty-object-type
export const websocketMiddleware: Middleware<{}, RootState> = store => next => action => {
  const result = next(action)
  const state = store.getState()
  const sessionId = Cookies.get("sessionId")
  const decoded = jwtDecode<jwtPayload>(sessionId || '')
  if (state.webSocket.client == null && state.webSocket.isConnected) {
    const client = new Client({
      brokerURL: `ws://localhost:8080/ws`,
      reconnectDelay: 5000,
    })
    client.onConnect = () => {
      store.dispatch(setConnectionStatus(true))
    }
    
    client.onDisconnect = () => {
      store.dispatch(setConnectionStatus(false))
    }
    client.activate()

    store.dispatch(setClient(client)) 
  }

  return result
}