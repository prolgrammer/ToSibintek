import { DownOutlined } from "@ant-design/icons"
import { Tree, TreeDataNode } from "antd"
import styled from "styled-components"

export const TreeRequests = () => {
  const treeData: TreeDataNode[] = [
    {
      title: 'parent 1',
      key: '0-0',
      children: [
        {
          title: 'parent 1-0',
          key: '0-0-0',
          children: [
            {
              title: 'leaf',
              key: '0-0-0-0',
            },
            {
              title: 'leaf',
              key: '0-0-0-1',
            },
            {
              title: 'leaf',
              key: '0-0-0-2',
            },
          ],
        },
        {
          title: 'parent 1-1',
          key: '0-0-1',
          children: [
            {
              title: 'leaf',
              key: '0-0-1-0',
            },
          ],
        },
        {
          title: 'parent 1-2',
          key: '0-0-2',
          children: [
            {
              title: 'leaf',
              key: '0-0-2-0',
            },
            {
              title: 'leaf',
              key: '0-0-2-1',
            },
          ],
        },
      ],
    },
  ]

  return (
    <Container>
      <h4>Дерево ответов: </h4>
      <Tree
        showLine
        switcherIcon={<DownOutlined />}
        defaultExpandedKeys={['0-0-0']}
        treeData={treeData}
      />
    </Container>
  )
} 

const Container = styled.div`
  display: flex;
  justify-content: left;
  align-items: top;
  flex-direction: column;
  padding: 3% 3% 3% 3%;
  background-color: white;
`