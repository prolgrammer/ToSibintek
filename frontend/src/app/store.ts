import { combineReducers, configureStore } from "@reduxjs/toolkit";
import { websocketMiddleware } from "./stomp";
import { webSocketSlice } from "@entities/webSocketSlice";
import { requestSlice } from "@widgets/ChatWindow";
// import { chatSlice } from "@entities/chatSlice";

const rootReducer = combineReducers({
  request: requestSlice.reducer,
  webSocket: webSocketSlice.reducer
})

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(websocketMiddleware),
})

export type RootState = ReturnType<typeof rootReducer>
export type AppDispatch = typeof store.dispatch
