import React from "react";

export default function FileUpload({ file, onChange }) {
  const inputId = "chat-file-input";

  return (
    <label className="file-upload">
      <span className="file-upload-title">Attach file</span>
      <div className="file-input-row">
        <input
          id={inputId}
          className="file-input-hidden"
          type="file"
          accept=".pdf,.txt,.md,.csv,.json,.log,image/*"
          onChange={(event) => {
            const selected = event.target.files?.[0] || null;
            onChange(selected);
          }}
        />
        <label htmlFor={inputId} className="file-trigger">
          {file ? "Change File" : "Choose File"}
        </label>
        <span className="file-name">{file ? file.name : "No file selected"}</span>
      </div>
      <small>PDF, text, or image</small>
    </label>
  );
}
