import { TypedUseSelectorHook, useSelector } from "react-redux";
import { RootState, store } from "./store";

export const useAppDispatch = () => store.dispatch
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;