import React, { useEffect, useState } from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import './css/MenuStyle.css';

import Button from 'react-bootstrap/Button';

import analysisimage from './analysis.png';

import axios from 'axios';

export default function Menu() {
  const [file, setFile] = useState(null);
  const [table_data, setTableData]=useState([]);
  const [cols, setCols] = useState([]);
  const [selected_cols, setSelectedCols] = useState({});
  const [preprocess, setPreprocess] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [view, setView] = useState("");
  const [algorithm, setAlgorithm] = useState("");
  const [problem, setProblem] = useState("");
  const [metricname, setMetricName] = useState("");
  const [metricvalue, setMetricValue] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [jsoninput, setJsonInput] = useState("");

  const FetchData = async (event) => {
    await axios.get('http://127.0.0.1:8000/fetch_data')
      .then(res_fetchdata => {
        setTableData(res_fetchdata.data);
        setCols(Object.keys(res_fetchdata.data[0]));
        
      })
      .catch(error => {
        console.error("No fetch data");
      });
  }

  const handleFileChange =async (event) => {
    setFile(event.target.files[0]);
  }; 

  const handleFileSubmit = async (event) => {
  event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post('http://127.0.0.1:8000/file_upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      FetchData();
    } catch (error) {
      console.error("Error uploading file:", error.response ? error.response.data : error.message);
    }
  };

  const handlecolChange = (event) => {
    const { name, checked } = event.target;
    setSelectedCols(prevState => ({
      ...prevState,
      [name]: checked 
    }));
    console.log(selected_cols);
  };

  const handlePreprocessSumit = () => {
    const formData = new FormData();
    formData.append('col',JSON.stringify(selected_cols));
    formData.append('prepros',preprocess);

    axios.post('http://localhost:8000/preprocess',formData)
    .then(res_preprocess => {
      setCols(Object.keys(res_preprocess.data[0]));
      setTableData(res_preprocess.data);
      console.log(cols);
      console.log(table_data);
      setSelectedCols({});
    })
    .catch(error => {
      console.error('No response of preprocess');
    });
  };

  const handlePreprocessChange = (value) => {
    setPreprocess(value);
  };

  const handleAnalysisSubmit = () => {
    setView("analysis");
    const formData = new FormData();
    formData.append('cols',JSON.stringify(selected_cols));
    formData.append('analysis',analysis);
    axios.post('http://localhost:8000/analysis',formData)
    .then(res_analysis => {
      console.log(res_analysis.data);
    })
    .catch(error => {
      console.error('No response of preprocess');
    });
  };

  const handleAnalysisChange = (value) => {
    setAnalysis(value);
  };

  const handleAlgorithmChange = (value) => {
    setAlgorithm(value);
  };

  const handleProblemChange =(event) => {
    setProblem(event.target.value);
  };

  const handleTrainSubmit = () => {
    setView("model_train");
    const formData = new FormData();
    formData.append('col',JSON.stringify(selected_cols));
    formData.append('algorithm',algorithm);
    formData.append('problem',problem);
    axios.post('http://localhost:8000/train',formData)
    .then(res_train => {
      setMetricValue(String(Object.values(res_train.data)[0]));
      setMetricName(Object.keys(res_train.data)[0]);
    })
    .catch(error => {
      console.error('No response of model train');
    });
  };

  const handlePickleSumit = () => {
    axios.get('http://localhost:8000/fetch_pickle')
    .then(res_pic => {
      
      if (res_pic.data.message == "success"){
        console.log(res_pic.data);
        const url = `${process.env.PUBLIC_URL}/model.pkl`; // Correct relative path
        const a = document.createElement('a');
        a.href = url;
        a.download = 'yourfile.pkl'; // Desired file name
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }
    })
    .catch(error => {
      console.error('No response of model train');
    });
  };

  const handlePredictEnable = (event) => {
    setView("predict");
    axios.get('http://localhost:8000/json_input')
    .then(res_input => {
      console.log(res_input.data);
      setJsonInput(res_input.data);
    })
    .catch(error => {
      console.error('No response of model train');
    });
  };

  const handleJsonInputChange =(event) => {
    setJsonInput(event.target.value);
  }

  const handlePredictSubmit = () =>{
    const formData = new FormData();
    formData.append('json_input',jsoninput);

    axios.post('http://localhost:8000/predictions',formData)
    .then(res_pic => {
      console.log(res_pic.data);
      setPrediction(res_pic.data.prediction)
    })
    .catch(error => {
      console.error('No response of prediction');
    });
  };

    return (
      <>
        <div class="row">
          <div class="col-2 doc">
          <h3>Load Data</h3>
          <div className='d-block'>
              <form onSubmit={handleFileSubmit}>
              <input type="file" onChange={handleFileChange} className='d-block'/><br/>
              <button type="submit" className='d-block'>Load Data</button>
              </form>
          </div><br/>

          <h3>Columns</h3>
          <div className='text-start'>
            {cols.length > 0 ? (
              cols.map((val, k) => (
                <label key={k} className='d-block'>
                  <input type="checkbox" name={val} onChange={handlecolChange} />
                  {val}
                </label>
              ))
            ) : (
              <p>No Columns</p>
            )}
          </div>
          </div>

          <div class="col-2 menu">
            
            <div className='preprocess'>
              <h3>Preprocess</h3>
              <div>
                <input type="radio" id="onehot_encode" value="onehot_encode" checked={preprocess === "onehot_encode"} onChange={() => handlePreprocessChange("onehot_encode")} />  
                <label htmlFor="option1">One hot encode </label>      
              </div>

              <div>
                <input type="radio" id="label_encode" value="label_encode" checked={preprocess === "label_encode"} onChange={() => handlePreprocessChange("label_encode")} />  
                <label htmlFor="option1">Label encode </label>      
              </div>

              <div>
                <input type="radio" id="drop_col" value="drop_col" checked={preprocess === "drop_col"} onChange={() => handlePreprocessChange("drop_col")} />  
                <label htmlFor="option1">Drop column</label>      
              </div>
              <Button onClick={handlePreprocessSumit}>Submit</Button>

            </div>

            <div className='analysis'>
              <h2>Analysis</h2>

              <div>
                <input type="radio" id="scatter_chart" value="scatter_chart" checked={analysis === "scatter_chart"} onChange={() => handleAnalysisChange("scatter_chart")} />  
                <label htmlFor="option1">Scatter chart</label>      
              </div>

              <div>
                <input type="radio" id="line_chart" value="line_chart" checked={analysis === "line_chart"} onChange={() => handleAnalysisChange("line_chart")} />  
                <label htmlFor="option1">Line chart </label>      
              </div>

              <Button onClick={handleAnalysisSubmit}>Submit</Button>
            </div> 

            <div className="model_train">
              <h3>Model</h3>
              <div>
                <input type="radio" id="logistic_regression" value="logistic_regression" checked={algorithm === "logistic_regression"} onChange={() => handleAlgorithmChange("logistic_regression")} />  
                <label htmlFor="option1">Logistic regression</label>      
              </div>

              <div>
                <input type="radio" id="decision_tree" value="decision_tree" checked={algorithm === "decision_tree"} onChange={() => handleAlgorithmChange("decision_tree")} />  
                <label htmlFor="option1">Decision Tree </label>      
              </div>

              <div>
                <input type="radio" id="random_forest" value="random_forest" checked={algorithm === "random_forest"} onChange={() => handleAlgorithmChange("random_forest")} />  
                <label htmlFor="option1">Random forest </label>      
              </div>

              <br/><div>
                <b>Select problem type</b>
                <select value={problem} onChange={handleProblemChange}>
                  <option value="">-- Choose Problem --</option>
                  <option value="regression">Regression Problem</option>
                  <option value="classification">Classification Problem</option>
                </select>
                {problem && <p>You selected: {problem}</p>}
              </div>
              <Button onClick={handleTrainSubmit}>Submit</Button>
            </div> <br/>

            <div className='prediction'>
              <h3>Prediction</h3>
              <Button onClick={handlePredictEnable}>Go predict</Button>
            </div>     

          </div>

          <div class="col-8 view">
            { (view.length==0 && (
              <div className='data_table'>
                <table className='table table-bordered' border="1">
                  <thead>
                    <tr>
                      {cols.map((item, index) => (
                        <th key={index}>{item}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {table_data.map((item, rowIndex) => (
                      <tr key={rowIndex}>
                        {cols.map((col, colIndex) => (
                          <td key={colIndex}>{item[col]}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              )) || (view.length==8 && (
                <div>
                  <b>Analysis image</b><br/>
                  <img src={analysisimage} alt="Analysis image"/>
                </div>
              )) || (view.length==11 && (
                <div>
                  <h3>Your Model Ready</h3>
                  <p>The model and pickle file ready</p>
                  <p>Model {metricname} is {metricvalue}</p>
                  <Button onClick={handlePickleSumit}>Download file</Button>
                </div>
              )) || (view.length==7 && (
                <div>
                  <p>Fill your input here</p>
                    <textarea id="json_input" value={jsoninput} onChange={handleJsonInputChange} name="json_input" rows="4" cols="50" /><br/>
                    <Button onClick={handlePredictSubmit}>Predict</Button>
                    <br/><br/>
                    <h2>The prediction value is :<b>{prediction}</b></h2>
                </div>
              ))
            }
          </div>
        </div>
      </>
    );
  
}
