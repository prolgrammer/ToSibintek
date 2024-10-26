import { combineReducers, configureStore } from "@reduxjs/toolkit";
import { websocketMiddleware } from "./stomp";
import { chatSlice } from "@pages/ExampleChat"
import { webSocketSlice } from "@entities/webSocketSlice";

const rootReducer = combineReducers({
  chat: chatSlice.reducer,
  webSocket: webSocketSlice.reducer
})

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(websocketMiddleware),
})

export type RootState = ReturnType<typeof rootReducer>
export type AppDispatch = typeof store.dispatch
