import React, { Component } from 'react';
import axios from 'axios';

const baseurl = "http://127.0.0.1:8000";

export default class Server extends Component{

    test(){
        window.alert("works")
    }

    file_upload(data){
       
        const res = axios.post('http://127.0.0.1:8000/file_upload', data, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

        return res;
    }
}