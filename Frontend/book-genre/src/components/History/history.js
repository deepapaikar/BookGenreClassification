import React from "react";
import "./history.css";
import bookFavicon from "../../assets/images/growth.png";

function History({ history }) {
  const fileHeaders = ["id", "file_name", "genre", "upload_date"];
  console.log();
  const downloadFile = (response, headers) => {
    const csvData = convertJSONToCSV(response, headers);
    const url = window.URL.createObjectURL(new Blob([csvData]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "yourfilename.csv");
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const convertJSONToCSV = (jsonData, columnHeaders) => {
    // Check if JSON data is empty
    if (jsonData.length === 0) {
      return "";
    }

    // Create headers string
    const headers = columnHeaders.join(",") + "\n";

    // Map JSON data to CSV rows
    const rows = jsonData
      .map((row) => {
        // Map each row to CSV format
        return columnHeaders.map((field) => row[field] || "").join(",");
      })
      .join("\n");

    // Combine headers and rows
    return headers + rows;
  };
  return (
    <div className="history-container">
      <h2>Recent</h2>
      <button className="submit-button" onClick={downloadFile(history, fileHeaders)}>
        Download History
      </button>
      <ul className="history-list">
        {history.map((item, index) => (
          <li key={index} className="history-item">
            <div className="history-left">
              <div className="history-logo">
                <img src={bookFavicon} alt="Logo" className="logo" />
              </div>
            </div>
            <div className="history-right">
              <div className="history-date-time">
                {new Date(item.upload_date).toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                  year: "numeric",
                })}{" "}
                {new Date(item.upload_date).toLocaleTimeString("en-US", {
                  hour: "numeric",
                  minute: "2-digit",
                  hour12: true,
                })}
              </div>
              <div className="history-name">
                {item.file_name.replace(".pdf", "")}{" "}
                {/* Remove .pdf extension */}
              </div>
              <div className="history-genre">{item.genre}</div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default History;
