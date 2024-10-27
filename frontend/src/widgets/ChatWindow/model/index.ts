import { createRequest } from "@entities/request"
import { createAsyncThunk, createSlice } from "@reduxjs/toolkit"

export const requestThunk = createAsyncThunk(
    'request/postRequest',
    async (request: string, { rejectWithValue }) => {
      return await createRequest(request)
        .then((response) => response)
        .catch((error) => rejectWithValue(error.response ? error.response.data : error.message))
    }
  )

export const requestSlice = createSlice({
    name: 'request',
    initialState: {
        error: null as string | null,
        loading: false
    },
    reducers: {},
    extraReducers: (builder) => {
        builder
        .addCase(requestThunk.pending, (state) => {
            state.error = null
            state.loading = true
        })
        .addCase(requestThunk.fulfilled, (state) => {
            state.error = null
            state.loading = false
        })
        .addCase(requestThunk.rejected, (state, action) => {
            state.error = action.payload as string
            state.loading = false
        })
    }
})