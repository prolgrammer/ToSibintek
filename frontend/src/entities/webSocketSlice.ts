import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Client } from '@stomp/stompjs';
import { RootState } from 'app/store';

interface WebSocketState {
  isConnected: boolean
  client: Client | null
}

const initialState: WebSocketState = {
  isConnected: false,
  client: null,
}

export const webSocketSlice = createSlice({
  name: 'webSocket',
  initialState,
  reducers: {
    connect(state) {
      state.isConnected = true
    },
    disconnect(state) {
      state.isConnected = false
    },
    setClient(state, action: PayloadAction<Client | null>) {
      state.client = action.payload
    },
    setConnectionStatus(state, action: PayloadAction<boolean>) {
      state.isConnected = action.payload
    },
  },
})

export const { connect, disconnect, setClient, setConnectionStatus } = webSocketSlice.actions
export const selectIsConnected = (state: RootState) => state.webSocket.isConnected
