import styled from "styled-components"
import bg from '@public/bgCity.svg'
import { Button, Flex } from "antd"
import { useNavigate } from "react-router-dom"
import logo from "@public/logo.svg"
import { SITES_NAME } from "@shared/constants"

export const WelcomeHero = () => {
  const navigate = useNavigate()
  return (
    <Container>
      <FlexContainer justify="space-between" align="center">
        <h3>
          <img src={logo} alt="logo" style={{marginRight: '10px'}}/>
          {SITES_NAME}
        </h3>
        <div>
          <Button
            type="primary"
            onClick={() => navigate('/chat')}
          >
            Попробовать
          </Button> 
        </div>
      </FlexContainer>
      <Content>
        <Title>
          Мы улучшили работу службы поддержки и готовы <br />
          обеспечить быстрые ответы на вопросы 
        </Title>
        <Button
          type="primary"
          block
          onClick={() => navigate('/chat')}
        >
          Сделать запрос
        </Button>
      </Content>
    </Container>
  )
}

const Container = styled.div`
  height: 700px;
  display: flex;
  flex-direction: column;
  gap: 25%;
  padding: 40px 130px;
  background: 
    linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.1)),
    url(${bg});
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  @media (max-width: 484px){
    gap:20px;
    padding:20px;
  }
  @media (max-width: 700px){
    gap:70px;
    padding:20px;
  }
  @media (max-width: 1000px){
    gap: 100px;
  }
`
const FlexContainer = styled(Flex)`
  h3 {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  @media (max-width: 484px) {
    flex-direction: column; 
    align-items: center; 
    gap: 10px; 
  }
`
  const Content = styled.div`
  text-align: center;
  margin: 0 auto;
  margin-bottom: 20%;
`
const Title = styled.h1`
  font-size: 40px;
  color: white;
  text-align: right;
  @media (max-width: 550px) {
    font-size: 30px;
  }
  @media (max-width: 420px) {
    font-size: 26px;
  }
`
