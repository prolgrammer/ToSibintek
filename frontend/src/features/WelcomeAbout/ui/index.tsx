import sign from '@public/icon/sign.svg'
import tree from '@public/icon/tree.svg'
import loop from '@public/icon/loop.svg'
import folder from '@public/icon/folder.svg'
import bg from '@public/whitebg.svg'
import styled from 'styled-components'

export const WelcomeAbout = () => {
  return (
    <Container>
      <Card>
        <h1>Найди ответ за считанные секунды</h1>
        <Grid>
          <CardLayout>
            <Icon src={sign} alt="sign icon" />
            <h2>
              Отправьте запрос  
            </h2>
            <Description>
              Заполните форму, указывая все атрибуты
            </Description>
          </CardLayout>
          
          <CardLayout>
            <Icon src={tree} alt="tree icon" />
            <h2>
              Определение ветки
            </h2>
            <Description>
              После отправки запроса, вы получите ответ на ваш вопрос
            </Description>
          </CardLayout>

          <CardLayout>
            <Icon src={loop} alt="loop icon" />
            <h2>
              Ищет решение из существующих 
            </h2>
            <Description>
              Выдается ответ
            </Description>
          </CardLayout>

          <CardLayout>
            <Icon src={folder} alt="folder   icon" />
            <h2>
              Находит решение из инструкции
            </h2>
            <Description>
              Просмотрите истории все своих обращений, их статус и предложенные решения
            </Description>
          </CardLayout>

        </Grid>
      </Card>
    </Container>
  )
}

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 8% 0 8%;
  background: 
    linear-gradient(rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)),
    url(${bg});
  background-size: cover;
  background-position: bottom;
  background-repeat: no-repeat;
  image-rendering: optimizeQuality;
  h1{
    @media (max-width: 725px) {
      font-size: 24px;
    }
    @media (max-width: 600px) {
      font-size: 20px;
    }
    @media (max-width: 400px) {
      font-size: 16px;
    }
  }
`
const Card = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  position: relative;
  bottom: 200px;
  border-radius: 30px;
  background-color: #FFD200;
  padding: 50px;
  @media (max-width: 600px) {
    padding: 30px; 
  }
`
const Grid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 22px;
  row-gap: 22px;
  @media (max-width: 725px) {
    grid-template-columns: 1fr; 
  }
`
const CardLayout = styled.div`
  padding: 20px;
  background: white;
  text-align: left;
  h2{
    color: black;
  }
  @media (max-width: 600px) {
    padding: 15px; 
    h2{
      font-size: 18px;
      }
  }
  @media (max-width: 400px) {
    h2{
      font-size: 14px;
      }
  }
`
const Description = styled.p`
  color: #999999;
  font-size: 14px;
  @media (max-width: 600px) {
    font-size: 12px;
  }
  @media (max-width: 400px) {
    font-size: 10px;
  }
`
const Icon = styled.img`
  @media (max-width: 725px) {
    width: 50px; 
  }
` 
