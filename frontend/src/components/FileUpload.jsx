import React from "react";

export default function FileUpload({ file, onChange }) {
  return (
    <label className="file-upload">
      <span className="file-upload-title">Attach file</span>
      <input
        type="file"
        accept=".pdf,.txt,.md,.csv,.json,.log,image/*"
        onChange={(event) => {
          const selected = event.target.files?.[0] || null;
          onChange(selected);
        }}
      />
      <small>{file ? file.name : "PDF, text, or image"}</small>
    </label>
  );
}
