import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [hotel, setHotel] = useState({
    location: '',
    checkInDate: '',
    checkOutDate: ''
  });
  const [loading, setLoading] = useState(false); // State variable to track loading state
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setHotel(prevState => ({
      ...prevState,
      [name]: value
    }));
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // Set loading state to true when form is submitted
    try {
      const response = await axios.post('http://localhost:5000/hotels', hotel);

      // Optionally, reset the form fields after successful submission
      setHotel({
        location: '',
        checkInDate: '',
        checkOutDate: ''
      });
    } catch (error) {
      console.error('Error sending data to server:', error);
    } finally {
      setLoading(false); // Reset loading state to false after submission completes
  }
  };
  return (
    <div className="container">
      <h1>{loading ? 'Loading...' : 'Book a hotel!'}</h1>
      <form className="form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Location:</label>
          <input type="text" name="location" value={hotel.location} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Check in date:</label>
          <input type="text" name="checkInDate" value={hotel.checkInDate} onChange={handleChange} placeholder='MM-DD-YY'/>
        </div>
        <div className="form-group">
          <label>Check out date:</label>
          <input type="text" name="checkOutDate" value={hotel.checkOutDate} onChange={handleChange} placeholder='MM-DD-YY'/>
        </div>
        <button className="btn" type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Submit'}
        </button>
      </form>
      {/* <div className='excel_file'>
        <a href='file:///E:/DataScience/WebScraping/newgithub/Hotel-Price-Scraper/server/requirements.txt' target='_blank'>Excel file...</a>
      </div> */}
    </div>
  );
}

export default App;
