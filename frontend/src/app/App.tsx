import { ConfigProvider as AntdProvider } from "antd"
import { Provider as ReduxProvider} from "react-redux"
import { RouterProvider } from "react-router-dom"
import ruRU from "antd/es/locale/ru_RU"
import { router } from "./router"
import { store } from "./store"

export const App = () => {
  const customTheme = {
    token: {
      colorPrimary: '#FFD200',
    },
  }

  return (
    <AntdProvider
      locale={ruRU}
      componentSize={"large"}
      getPopupContainer={(trigger: any) => trigger?.parentElement}
      theme={customTheme}
    >
      <ReduxProvider store={store}>
        <RouterProvider router={router} />
      </ReduxProvider>
    </AntdProvider>
  )
}
