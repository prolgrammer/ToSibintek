import { axiosInstance } from "@shared/api"

export const createRequest= (request: string) => {
  return axiosInstance.request({
    url: '/requests',
    method: 'post',
    data: request,
  }).catch(error => console.error(error))
}