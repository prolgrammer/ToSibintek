import { getSession } from "@entities/session"
import { TreeRequests } from "@features/TreeRequests"
import { ChatWindow } from "@widgets/ChatWindow"
import { Splitter } from "antd"
import { useEffect } from "react"
import styled from "styled-components"
import Cookies from "js-cookie"
import { useDispatch } from "react-redux"
import { AppDispatch } from "app/store"
import { webSocketSlice } from "@entities/webSocketSlice"

export const ExampleChatPage = () => {
  const dispatch: AppDispatch = useDispatch()

  useEffect( () => {
    const fetchSession = async () => {
      try {
        const response = await getSession()
        Cookies.set("sessionId", response)
      } catch (error) {
        console.error(error)
      }
    }

    dispatch(webSocketSlice.actions.connect())

    fetchSession()
  }, [dispatch])

  return (
    <>
      <Splitter>
        <Splitter.Panel collapsible>
          <ChatWindow />
        </Splitter.Panel>
        <Splitter.Panel>
          <Splitter layout="vertical">
            <Splitter.Panel>
              <TreeRequests />
            </Splitter.Panel>
            <Splitter.Panel>
              <Container>
                <h4>Журнал работы:</h4>
              </Container>
            </Splitter.Panel>
          </Splitter>
        </Splitter.Panel>
      </Splitter>
    </>
  )
}

const Container = styled.div`
  display: flex;
  justify-content: left;
  align-items: top;
  padding: 3% 3% 3% 3%;
  background-color: white;
`
