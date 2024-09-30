import React, { useState, useEffect } from "react";
import UploadFile from "./components/UploadFile/uploadFile";
import History from "./components/History/history";
import "./App.css";

function App() {
  const [book, setBook] = useState(null);
  const [genre, setGenre] = useState("");
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);



  // Function to fetch history data from the backend
  const fetchHistory = async () => {
    try {
      const response = await fetch("http://localhost:4000/history");
      const data = await response.json();
      console.log("Fetched History:", data);
      setHistory(data);
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  };
   // Function to fetch history data from the backend
   const DownloadHistory = async () => {
    try {
      const response = await fetch("http://localhost:4000/history");
      const data = await response.json();
      console.log("Fetched History:", data);
      setHistory(data);
  
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  };
  const handleDownload= async()=>{
    DownloadHistory();

  }

  // Fetch the history when the component mounts
  useEffect(() => {
    fetchHistory(); // Call the fetch function when the component mounts
  }, []);

  // Handle file upload from UploadFile component
  const handleFileUpload = (file) => {
    console.log("File uploaded:", file);
    setBook(file);
  };

  // Handle form submission and upload process
  const handleSubmit = async () => {
    if (!book) {
      alert("Please upload a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", book);

    try {
      // Upload file to the backend and get genre
      const response = await fetch("http://localhost:4000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        // Set the detected genre from the backend
        const detectedGenre = data.genre;
        setGenre(detectedGenre);

        // Fetch the updated history after a successful upload
        await fetchHistory(); // Re-fetch the history to update the panel

        // Reset the book and genre states
        setBook(null);
        setGenre("");
      } else {
        console.error("Error uploading file:", data.message);
      }
    } catch (error) {
      console.error("Error submitting file:", error);
    }
  };

  return (
    <div className="app">
      <div className="left-panel">
        {/* Pass the fetched history data to the History component */}
        <History history={history}/>
      </div>
      <div className="main-panel">
        {/* Pass the file and submit handler to the UploadFile component */}
        <UploadFile
          history={history}
          onUpload={handleFileUpload}
          book={book}
          onSubmit={handleSubmit}
        />
      </div>
    </div>
  );
}

export default App;
