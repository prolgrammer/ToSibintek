import styled from "styled-components"
import bg from '@public/bgCity.svg'
import { Button, Flex } from "antd"
import { useNavigate } from "react-router-dom"

export const WelcomeHero = () => {
  const navigate = useNavigate()
  return (
    <Container>
      <FlexContainer justify="space-between" align="center">
        <h3>Deadline Destroyers ©</h3>
        <div>
          <Button
            type="primary"
            size="large"
            onClick={() => navigate('/chat')}
          >
            Попробовать
          </Button>
        </div>
      </FlexContainer>
      <Content>
        <Title>
          Dedline Destroyers v1.0
        </Title>
        <SubTitle>
          Мы оптимизировали работу службы поддержки и
          готовы обеспечить быстрые ответы на
          вопросы пользовтелей
        </SubTitle>
        <Button
          type="primary"
          block
          onClick={() => navigate('/chat')}
          size="large"
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
  padding: 40px;
  background: 
    linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)),
    url(${bg});
  background-size: cover;
  background-position: center;
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
  @media (max-width: 484px) {
    flex-direction: column; 
    align-items: center; 
    gap: 10px; 
  }
`
const Content = styled.div`
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
  margin-bottom: 20%;
`
const Title = styled.h1`
  font-size: 40px;
  color: white;
  text-align: center;
  @media (max-width: 550px) {
    font-size: 30px;
  }
  @media (max-width: 420px) {
    font-size: 26px;
  }
`
const SubTitle = styled.h3`
  color: #9FA1AD;
  text-align: center;
   @media (max-width: 550px) {
    font-size: 16px; 
  }
`