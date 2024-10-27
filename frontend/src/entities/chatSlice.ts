import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Message {
  request: string
  time: string
  stage: string
  service: string
  solution: string
}

interface ChatState {
  messages: Message[]
}

const initialState: ChatState = {
  messages: [],
}

export const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage(state, action: PayloadAction<Message>) {
      state.messages.push(action.payload)
    },
  },
})

export const { addMessage } = chatSlice.actions
