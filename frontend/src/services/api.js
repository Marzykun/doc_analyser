import axios from 'axios'

const API_BASE = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'multipart/form-data'
  }
})

export const uploadContract = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post('/analyze/', formData)
  return response.data
}

export const getAnalysisHistory = async () => {
  const response = await axios.get(`${API_BASE}/history`)
  return response.data
}

export default api
