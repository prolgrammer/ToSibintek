import axios from "axios"
import { API_URL } from "./constants"
import Cookies from "js-cookie"

export const axiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 1000,
  headers: {
    'Authorization': 'Bearer ' + Cookies.get('sessionId'),
  },
  withCredentials: true
})
