import React from 'react';
import 'antd/dist/antd.css';
import '../index.css';
import Uploadpage from "./upload"
import Mymenu from "./display"

class My_app extends React.Component{
  state={
    display_page:"upload"
  }
  json_from_backend=[]
  prob=0
  

   getmesg = (json,prob,state_change)=>{
     this.json_from_backend=json
     this.prob=prob
     
     this.setState({
       
       display_page:state_change
     })
     
   }
   render(){
     var page
     if(this.state.display_page=="upload"){
       page=<Uploadpage getmesg={this.getmesg} />
     }
     if(this.state.display_page=="display"){
      
      page=<Mymenu json_paperid_keyword={this.json_from_backend} prob={this.prob} />
     }

     return page
   }
}

export default My_app