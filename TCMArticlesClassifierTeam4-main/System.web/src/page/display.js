
import React from 'react';
import 'antd/dist/antd.js';
import 'antd/dist/antd.css';
import { Menu, Table, Progress, Layout, Button,Space,Input, } from 'antd';
import Highlighter from 'react-highlight-words';
import { SearchOutlined } from '@ant-design/icons';
import My_app from "./main_home"
import './display.css'
const { Content, Sider, Header } = Layout;


function Probability(props) {
    var percent = (props.prob * 100).toFixed(2)
    return (
        <Layout>
            
             <header className="prob_title">   probability of keyword inside the title to represent that it is a tcm article</header>
            
            <Content>
                <Progress className="pie" 
                  type="circle" 
                  strokeColor= {{
                    "0%": "#62A755",
                    "100%": "#108ee9" }}
                  trailColor="white"
                  strokeWidth="13"
                    percent={percent}
                    width="400px"  />
            </Content>
        </Layout>
    )

}

class Mymenu extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            displaypage: 'keyword',
            backtoupload_page: false,
            searchText: '',
            searchedColumn: '',
        };



    }
    getColumnSearchProps = dataIndex => ({
        filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters }) => (
          <div style={{ padding: 8 }}>
            <Input
              ref={node => {
                this.searchInput = node;
              }}
              placeholder={`Search ${dataIndex}`}
              value={selectedKeys[0]}
              onChange={e => setSelectedKeys(e.target.value ? [e.target.value] : [])}
              onPressEnter={() => this.handleSearch(selectedKeys, confirm, dataIndex)}
              style={{ marginBottom: 8, display: 'block' }}
            />
            <Space>
              <Button
                type="primary"
                onClick={() => this.handleSearch(selectedKeys, confirm, dataIndex)}
                icon={<SearchOutlined />}
                size="small"
                style={{ width: 90 }}
              >
                Search
              </Button>
              <Button onClick={() => this.handleReset(clearFilters)} size="small" style={{ width: 90 }}>
                Reset
              </Button>
              <Button
                type="link"
                size="small"
                onClick={() => {
                  confirm({ closeDropdown: false });
                  this.setState({
                    searchText: selectedKeys[0],
                    searchedColumn: dataIndex,
                  });
                }}
              >
                Filter
              </Button>
            </Space>
          </div>
        ),
        filterIcon: filtered => <SearchOutlined style={{ color: filtered ? '#1890ff' : undefined }} />,
        onFilter: (value, record) =>
          record[dataIndex]
            ? record[dataIndex].toString().toLowerCase().includes(value.toLowerCase())
            : '',
        onFilterDropdownVisibleChange: visible => {
          if (visible) {
            setTimeout(() => this.searchInput.select(), 100);
          }
        },
        render: text =>
          this.state.searchedColumn === dataIndex ? (
            
            <Highlighter
              highlightStyle={{ backgroundColor: '#ffc069', padding: 0 }}
              searchWords={[this.state.searchText]}
              autoEscape
              textToHighlight={text ? text.toString() : ''}
            />
          ) : (
            text
          ),
      });
    
      handleSearch = (selectedKeys, confirm, dataIndex) => {
        confirm();
        this.setState({
          searchText: selectedKeys[0],
          searchedColumn: dataIndex,
        });
      };
    
      handleReset = clearFilters => {
        clearFilters();
        this.setState({ searchText: '' });
      };




    handleClick = e => {

        if (e.key == '1') {
            this.setState({
                displaypage: 'keyword'
            })
        }
        else {
            this.setState({
                displaypage: 'prob'
            })
        }

    }

    backtoupload = e => {
        fetch('/cancel_task')
        .then(res => res.text())
        .then(res => {
            alert(res);
          
        })
        
        this.setState({
            
            
                backtoupload_page:true
            
        })
 
    }
    render() {
        
        if (this.state.backtoupload_page == false) {
            let page;

            if (this.state.displaypage == 'keyword') {
                
                    const columns = [
                        {
                            title: 'Title',
                            dataIndex: 'Title',
                            ...this.getColumnSearchProps('Title'),
                        }
                        ,
                
                        {
                            title: 'keyword',
                            dataIndex: 'keyword',
                            ...this.getColumnSearchProps('keyword'),
                
                
                        },
                
                    ];
                
                page=<Table columns={columns} dataSource={this.props.json_paperid_keyword} />
            

                }
            else if (this.state.displaypage == 'prob') {
                page = <Probability prob={this.props.prob} />;
            }


            return (

                <Layout className="b">
                    <Sider width={200}>
                        <Menu
                            onClick={this.handleClick}
                            style={{ height: '100%', borderRight: 0 }}
                            defaultSelectedKeys={['1']}
                            mode="inline"

                        >
                            <Menu.Item key="1">
                                keyword
                            </Menu.Item>
                            <Menu.Item key="2">
                                prob
                            </Menu.Item>
                        </Menu>
                    </Sider>
                    <Content className="content">

                        {page}

                        <Button className='upload_again' onClick={this.backtoupload}>upload_again </Button>


                    </Content>
                </Layout>
            )
        }
        else{
            return <My_app />
        }
    }

}
export default Mymenu
