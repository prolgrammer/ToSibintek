import { Button, Layout } from "antd"
import { Content, Header } from "antd/es/layout/layout"
import { ReactNode } from "react"
import styled from "styled-components"

export const MainLayout = ({children} : {children: ReactNode}) => {
  return (
    <Layout style={{height: '100vh'}}>
      <HeaderWrapper>
        <h3>
          Облачный помощник
        </h3>
        <Button>Попробовать</Button>
      </HeaderWrapper>
      <Layout>
        <Wrapper>
          {children}
        </Wrapper>
      </Layout>
    </Layout>
  )
}

const HeaderWrapper = styled(Header)`
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: transparent;
`
const Wrapper = styled(Content)`
  display: flex;
  justify-content: center;
  align-items: center;
`
