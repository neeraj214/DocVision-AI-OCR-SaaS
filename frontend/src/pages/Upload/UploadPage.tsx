import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, X, File as FileIcon, AlertCircle, Loader2 } from "lucide-react";
import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { ResultsDisplay } from "../../components/ResultsDisplay";
import { cn } from "../../components/ui/Button";
import { getToken, isTokenExpired } from "../../services/api";

export const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState<any | null>(null);

  const onDrop = (acceptedFiles: File[]) => {
    setError(null);
    setResult(null);
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".png", ".jpg", ".jpeg"],
    },
    maxFiles: 1,
    multiple: false,
    maxSize: 10 * 1024 * 1024,
  });

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const token = getToken();
      if (!token || isTokenExpired(token)) {
        throw new Error("Please login to continue");
      }
      const response = await fetch("http://localhost:8000/api/ocr/routed", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to process image");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsUploading(false);
    }
  };

  const clearFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    setFile(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-slide-up">
      <div className="text-center space-y-4">
        <h2 className="text-3xl font-bold text-text-neutral">Upload Document</h2>
        <p className="text-text-secondary">
          Supported formats: PNG, JPG, JPEG. Max file size: 10MB.
        </p>
      </div>

      <Card className="p-1">
        <div
          {...getRootProps()}
          className={cn(
            "border-2 border-dashed rounded-xl p-12 transition-all duration-300 cursor-pointer flex flex-col items-center justify-center text-center min-h-[300px]",
            isDragActive
              ? "border-action-primary bg-action-primary/10"
              : "border-white/10 hover:border-white/20 hover:bg-white/5",
            file ? "bg-white/5 border-solid border-white/10" : ""
          )}
        >
          <input {...getInputProps()} />
          
          {file ? (
            <div className="relative group w-full max-w-sm">
              <div className="absolute -top-3 -right-3">
                <button
                  onClick={clearFile}
                  className="p-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-full transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              
              <div className="flex flex-col items-center gap-4">
                <div className="relative w-20 h-20 bg-primary-base rounded-lg flex items-center justify-center shadow-lg border border-white/10">
                  <FileIcon className="w-8 h-8 text-action-primary" />
                  {file.type.startsWith("image/") && (
                    <img
                      src={URL.createObjectURL(file)}
                      alt="Preview"
                      className="absolute inset-0 w-full h-full object-cover rounded-lg opacity-50"
                    />
                  )}
                </div>
                <div className="text-left w-full bg-white/5 p-4 rounded-lg border border-white/5">
                  <p className="font-medium text-text-neutral truncate">{file.name}</p>
                  <p className="text-sm text-text-secondary">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="w-16 h-16 bg-action-primary/10 rounded-full flex items-center justify-center mx-auto ring-1 ring-action-primary/20">
                <Upload className="w-8 h-8 text-action-primary" />
              </div>
              <div>
                <p className="text-lg font-medium text-text-neutral">
                  Drag & drop your file here
                </p>
                <p className="text-text-secondary mt-1">or click to browse</p>
              </div>
            </div>
          )}
        </div>
      </Card>

      {error && (
        <div className="flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/20 text-red-200 rounded-lg animate-fade-in">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <p>{error}</p>
        </div>
      )}

      <div className="flex justify-center">
        <Button
          onClick={handleUpload}
          disabled={!file || isUploading}
          size="lg"
          className="w-full sm:w-auto min-w-[200px]"
        >
          {isUploading ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              Processing...
            </>
          ) : (
            "Process Document"
          )}
        </Button>
      </div>

      {result && (
        <div className="animate-slide-up">
          <ResultsDisplay result={result} />
        </div>
      )}
    </div>
  );
};

export default UploadPage;
