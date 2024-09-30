// UploadFile.js
import React, { useState } from "react";
import "./uploadFile.css";
import bookLogo from "../../assets/images/book_favicon.png"; // Sample book logo
import questionMark from "../../assets/images/question_mark.jpg";

function UploadFile() {
  const [file, setFile] = useState(null);
  const [genre, setGenre] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [download, setDownload]= useState(null)

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };
  const downloadFile=(event)=>{
    setDownload(event.target.files[0]);
  }
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert("Please upload a file first!");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    try {
      // Send file to the backend
      const response = await fetch("http://localhost:4000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        // Set the genre received
        setGenre(data.genre);
        setSubmitted(true);
      } else {
        alert("Error uploading file");
        console.error("Error:", data.message);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="upload-container">
      <div className="left-section">
        <div className="upload-heading">Guess the genre</div>
        <div className="upload-description">
          Upload the PDF file of your book to find out if it's Fiction,
          Non-fiction, or Romance.
        </div>
        <div className="upload-title">Upload a PDF</div>
        <input
          type="file"
          className="upload-input"
          accept="application/pdf"
          onChange={handleFileUpload}
        />
        <button className="submit-button" onClick={handleSubmit}>
          Submit
        </button>
      </div>

      <div className="right-section">
        {!submitted ? (
          <div className="placeholder">
            <img
              src={questionMark}
              alt="Question Mark"
              className="question-mark"
            />
          </div>
        ) : (
          <div className="card">
            <img src={bookLogo} alt="Book Logo" className="book-logo" />
            <div className="book-genre">
              The genre of the book is <strong>{genre}</strong>
            </div>
          </div>
          
        )}
       
      </div>
    </div>
  );
}

export default UploadFile;
