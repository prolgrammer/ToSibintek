import { API_URL } from "@shared/constants"
import axios from "axios"

export const getSession= () => {
  return axios.request({
    url: `${API_URL}/generate-session`,
    method: 'get'
  })
  .then(response => response.data)
  .catch(error => console.error(error))
}