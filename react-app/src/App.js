import React from "react";
import {useState, useEffect} from "react";
import DatetimeRangePicker from "react-datetime-range-picker";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend } from 'recharts';


function App() {
  const [start_date, setStartDate] = useState(new Date())
  const [end_date, setEndDate] = useState(new Date())
  const [data, setData] = useState([{}])

  const getTurbineData = async (start, end) => {
    const response = await axios.get("http://localhost:8000/turbine/1", { params:  {
      start_date: ('0' + start.getDate()).slice(-2) + '.'+ ('0' + (start.getMonth()+1)).slice(-2) + '.' + start.getFullYear() + ' 00:00',
      end_date: ('0' + end.getDate()).slice(-2) + '.'+ ('0' + (end.getMonth()+1)).slice(-2) + '.' + end.getFullYear() + ' 23:59'
    }});
    let sorted_data = sort_turbin_data(response.data, 'Wind m/s')
    sorted_data.map((x) => x['Leistung kW'] = parseFloat(x['Leistung kW']))
    sorted_data.map((x) => x['Wind m/s'] = parseFloat(x['Wind m/s']))
    setData(sorted_data)
  }

  const sort_turbin_data = (data, key) => {
    return data.sort((a, b) => parseFloat(a[key].replace(',','.')) - parseFloat(b[key].replace(',','.')))
  }

  useEffect(()=>{
    let startDate = new Date('January 01, 2016')
    let endDate = new Date('March 31, 2016')
    setStartDate(startDate)
    setEndDate(endDate)
    getTurbineData(startDate, endDate)
  }, []) 


  let handler = daterange => {
    setStartDate(daterange['start'])
    setEndDate(daterange['end'])
    getTurbineData(daterange['start'], daterange['end'])
  }

  return (
    <div className="App">
      <div>
        <h3>Pick the date time range</h3>
        <DatetimeRangePicker
          onChange={handler} 
          timeFormat={false} 
          startDate={start_date}
          endDate={end_date}
        />
        <LineChart width={700} height={500} data={data}>
          <XAxis dataKey="Wind m/s" />
          <YAxis dataKey="Leistung kW" />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="Leistung kW"
            stroke="#8884d8"
          />
        </LineChart>
      </div>
    </div>
  );
}

export default App;