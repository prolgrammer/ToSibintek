import { TreeRequests } from "@features/TreeRequests"
import { ChatWindow } from "@widgets/ChatWindow"
import { Splitter } from "antd"
import styled from "styled-components"

export const ExampleChatPage = () => {
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
