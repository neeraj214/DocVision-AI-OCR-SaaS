import React from "react";

const HomePage: React.FC = () => {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-slate-900">
        Welcome to DocVision AI
      </h2>
      <p className="text-slate-600">
        This is a placeholder home page. In upcoming steps, you will be able
        to upload images and extract text using our OCR pipeline.
      </p>
    </div>
  );
};

export default HomePage;

