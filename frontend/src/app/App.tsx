import { ConfigProvider as AntdProvider } from "antd"
import { Provider as ReduxProvider} from "react-redux"
import { RouterProvider } from "react-router-dom"
import { router } from "./router"
import { store } from "./store"

export const App = () => {
  return (
    <AntdProvider>
      <ReduxProvider store={store}>
        <RouterProvider router={router} />
      </ReduxProvider>
    </AntdProvider>
  )
}
