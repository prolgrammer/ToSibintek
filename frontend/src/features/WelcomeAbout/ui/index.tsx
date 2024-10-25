// import chatIcon from '@public/icon/chat-icon.svg'
// import uploadIcon from '@public/icon/upload-icon.svg'
// import codeIcon from '@public/icon/code-icon.svg'
// import messageIcon from '@public/icon/message-icon.svg'
// import bgIntegration from '@public/bg-Integration.svg'
import styled from 'styled-components'

export const WelcomeAbout = () => {
  return (
    <Container>
      <Card>
        <h1>Найди ответ за считанные секунды</h1>
        <Grid>
          <CardLayout>
            {/* <Icon src={chatIcon} alt="chat icon" /> */}
            <h2>
              Пройди регистрацию
            </h2>
            <Description>
              Пройди регистрацию и получи уникальный токен, который понадобиться для интеграции чат-бота на своем сайте
            </Description>
          </CardLayout>
          
          <CardLayout>
            {/* <Icon src={uploadIcon} alt="upload icon" /> */}
            <h2>
              Пройди регистрацию
            </h2>
            <Description>
              Пройди регистрацию и получи уникальный токен, который понадобиться для интеграции чат-бота на своем сайте
            </Description>
          </CardLayout>

          <CardLayout>
            {/* <Icon src={codeIcon} alt="code icon" /> */}
            <h2>
              Пройди регистрацию
            </h2>
            <Description>
              Пройди регистрацию и получи уникальный токен, который понадобиться для интеграции чат-бота на своем сайте
            </Description>
          </CardLayout>

          <CardLayout>
            {/* <Icon src={messageIcon} alt="message icon" /> */}
            <h2>
              Пройди регистрацию
            </h2>
            <Description>
              Пройди регистрацию и получи уникальный токен, который понадобиться для интеграции чат-бота на своем сайте
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
  padding: 5% 8% 5% 8%;

  .title{
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
  border-radius: 10px;
  background-color: #FFD200;
  padding: 50px;
  @media (max-width: 600px) {
    padding: 30px; 
  }
`
const Grid = styled.div`
  display: grid;
  grid-template-columns: auto auto;
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
    color:#ffffff;
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