import { WelcomePage } from "@pages/WelcomePage/ui";
import { createBrowserRouter } from "react-router-dom";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <WelcomePage />
  }
])