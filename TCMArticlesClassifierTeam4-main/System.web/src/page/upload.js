import React from 'react';
//import 'antd/dist/antd.css';
import { Form, Upload, Button, message } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import './upload.css'


class Uploadpage extends React.Component {

  state = {
    filelist: []
  }
  url_get_result = ''
  status = ''
  

  uploadready = (e) => {
    const { filelist } = this.state
    const formData = new FormData()
    filelist.forEach(file => {

      formData.append('file[]', file)

    })

    this.post("/predict", formData)
    
    

  }
  handleresponse=(res)=>{

    return res.json()
    .then(json=>{
      
      
      if(json["status"]=='error'){
        this.status='error'
        return Promise.reject(json)
      }else{
        return json
      }
    })
  }

  post = (url, data) => {  //而post函数，不仅指定api，还需要从前端传递参数信息过来
    return new Promise((resolve, reject) => {
      
      fetch(url, {
        method: 'POST',
        body: data

      })
        .then(res =>res.json())
        .then(res => {
          
          

          this.url_get_result = res['Location']
          
          var start = setInterval(  repeatget => {
             
            if (this.status == 'done' || this.status == 'stop'||this.status=='error') {
              this.status=''
              clearInterval(start)
              return
            }
            this.get( this.url_get_result )
            
          }, 2000)

        })
        .catch(error => {
          if (error=="TypeError: Failed to fetch"){
            message.error("please reselect all of your files")
          }
          reject(error);
        })
    })
  }
  
  get = (url) => {
    return new Promise((resolve, reject) => {
      fetch(url)
        .then(this.handleresponse)
        .then(res => {

          this.status = res['status']
          
          const { getmesg } = this.props

          getmesg(res["finished"], res["prob"], "display")
        })
        .catch(error => {
          
          message.error(error["message"]);
          reject()
        })
    })
  }

  beforeUploadrewrite = file => {
    const isCSV = file.type === 'application/vnd.ms-excel';

    if (!isCSV) {
      message.error(`${file.name} is not a csv file`);
      return isCSV || Upload.LIST_IGNORE;
    }
    this.setState(state => {
      const newFileList = state.filelist.slice();
      newFileList.push(file)
      return {
        filelist: newFileList
      }

    })
    
    return false
  }

  Removefile = file => {
    this.setState(state => {
      const index = state.filelist.indexOf(file);
      const newFileList = state.filelist.slice();
      newFileList.splice(index, 1);
      return {
        filelist: newFileList,
      };
    });
  }


  render() {
    return (
      <div className='box'>
        <h1 className="title"> 
          Traditional Chinese Medicine Article Classifier 
          </h1>
          <img className="logo" src="https://i.imgur.com/m1N5xwg.png"></img>
        <form className='form'>
          <Form.Item name="dragger" noStyle>
            <Upload.Dragger className="drop-space" name="files" beforeUpload={this.beforeUploadrewrite} onRemove={this.Removefile}>
              <p className="ant-upload-drag-icon">
                <InboxOutlined />
              </p>
              <p className="ant-upload-text">Click or drag file to this area to upload</p>
              <p className="ant-upload-hint">only accept .csv file as classified article</p>
            </Upload.Dragger>
          </Form.Item>

          </form>
            <Button className="button" type="primary" htmlType="submit" onClick={this.uploadready}>
              UPLOAD
            </Button>
      </div>

    )


  }
}

export default Uploadpage