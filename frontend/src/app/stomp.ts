import { Middleware } from '@reduxjs/toolkit';
import { Client } from '@stomp/stompjs';
import { RootState } from '../app/store';
import { setClient, setConnectionStatus } from '@entities/webSocketSlice';
import { jwtDecode } from 'jwt-decode';
import Cookies from "js-cookie"

// // eslint-disable-next-line @typescript-eslint/no-empty-object-type
// const websocketMiddleware: Middleware<{}, RootState> = (storeAPI) => {
//   let client: Client | null = null;

//   return (next) => (action) => {
//     switch (action.type) {
//       case connect.type:
//         client = new Client({
//           brokerURL: 'ws://your-server-url/websocket',
//           reconnectDelay: 5000,
//         })

//         client.onConnect = () => {
//           storeAPI.dispatch(setConnectionStatus(true))

//           client?.subscribe('/topic/chat', (message: IMessage) => {
//             const parsedMessage = JSON.parse(message.body)
//             storeAPI.dispatch(addMessage(parsedMessage))
//           })
//         }

//         client.onDisconnect = () => {
//           storeAPI.dispatch(setConnectionStatus(false))
//         }

//         client.activate()
//         break;

//       case disconnect.type:
//         if (client) {
//           client.deactivate()
//           client = null
//           storeAPI.dispatch(setConnectionStatus(false))
//         }
//         break;

//       default:
//         break;
//     }

//     return next(action)
//   }
// }

// export default websocketMiddleware
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
      brokerURL: `ws://localhost:8080/users/${decoded.id}/queue/messages`,
      reconnectDelay: 5000,
    })
    client.onConnect = () => {
      store.dispatch(setConnectionStatus(true))
    }
    client.onDisconnect = () => {
      store.dispatch(setConnectionStatus(false))
    }
    client.activate()

    store.dispatch(setClient(true))
  }

  return result
}