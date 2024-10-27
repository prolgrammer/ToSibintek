import { SITES_NAME } from "@shared/constants";
import { Input } from "antd";
import { useState, useEffect } from "react";
import styled from "styled-components";
import logo from "@public/logo.svg";
import { AppDispatch, RootState } from "app/store";
import { useDispatch, useSelector } from "react-redux";
import { requestThunk } from "../model";

export const ChatWindow = () => {
  const [messages, setMessages] = useState<string[]>([])
  const [input, setInput] = useState<string>("")
  // const [loading, setLoading] = useState<boolean>(false)
  const dispatch: AppDispatch = useDispatch()
  const { error, loading} = useSelector((state: RootState) => state.request)
  const { Search } = Input

  const sendMessage = (message: string) => {
    if (message.trim()) {
      setMessages((prevMessages) => [...prevMessages, error ? error : `Вы: ${message}`])
      dispatch(requestThunk(message))
      setInput("")
      // setLoading(true)

      setTimeout(() => {
        setMessages((prevMessages) => [...prevMessages, "Бот: This is a response!"])
        // setLoading(false)
      }, 1000)
    }
  }

  useEffect(() => {
    const chatWindow = document.getElementById("chatWindow")
    if (chatWindow) {
      chatWindow.scrollTop = chatWindow.scrollHeight
    }
  }, [messages])

  return (
    <Container>
      <Logo>
        <img src={logo} alt="logo" style={{marginRight: '10px'}}/>
        {SITES_NAME}
      </Logo>
      <Card>
        <Window id="chatWindow">
          {messages.map((msg, index) => (
            <Message key={index} isBot={msg.startsWith("Бот:")}>
              {msg}
            </Message>
          ))}
        </Window>
      </Card>
      <Search
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Что делать?"
        enterButton={"Отправить"}
        onSearch={() => sendMessage(input)}
        loading={loading}
      />
    </Container>
  )
}

const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: white;
  padding: 5% 10% 10% 10%;
`
const Logo = styled.h1`
  display: flex;
  justify-content: left;
  align-items: center;
`
const Card = styled.div`
  border-radius: 30px;
  background: linear-gradient(rgba(235, 173, 0, 0.6) , rgba(255, 210, 0, 0));
  padding: 35px 45px;
  width: 100%;
  margin-bottom: 5%;
`
const Window = styled.div`
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  background-color: white;
  border-radius: 10px;
  padding: 10px;
  height: 200px;
`
const Message = styled.div<{ isBot: boolean }>`
  background-color: ${({ isBot }) => (isBot ? "#EBAD00" : "#C7C7C7")};
  margin: 10px 0;
  padding: 12px;
  border-radius: ${({ isBot }) => (isBot ? "0 20px 20px 20px" : "20px 0  20px 20px")};
  max-width: 60%;
  align-self: ${({ isBot }) => (isBot ? "flex-start" : "flex-end")};
  color: ${({ isBot }) => (isBot ? "black" : "white")};
  word-wrap: break-word;
`
