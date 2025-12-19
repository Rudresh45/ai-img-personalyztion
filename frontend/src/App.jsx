import { useState } from 'react';
import UploadForm from './components/UploadForm';
import ProcessingStatus from './components/ProcessingStatus';
import ResultDisplay from './components/ResultDisplay';
import './index.css';

function App() {
  const [currentStep, setCurrentStep] = useState('upload'); // upload, processing, result
  const [requestId, setRequestId] = useState(null);
  const [resultData, setResultData] = useState(null);
  const [error, setError] = useState(null);

  const handleUploadComplete = (id) => {
    setRequestId(id);
    setCurrentStep('processing');
    setError(null);
  };

  const handleProcessingComplete = (data) => {
    setResultData(data);
    setCurrentStep('result');
  };

  const handleProcessingError = (errorMessage) => {
    setError(errorMessage);
    setCurrentStep('upload');
  };

  const handleTryAgain = () => {
    setCurrentStep('upload');
    setRequestId(null);
    setResultData(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>✨ AI Photo Personalization</h1>
        <p className="app-subtitle">
          Transform your child's photo into a beautiful illustrated character
        </p>
      </header>

      <main className="container">
        {currentStep === 'upload' && (
          <UploadForm 
            onUploadComplete={handleUploadComplete}
            error={error}
          />
        )}

        {currentStep === 'processing' && (
          <ProcessingStatus
            requestId={requestId}
            onComplete={handleProcessingComplete}
            onError={handleProcessingError}
          />
        )}

        {currentStep === 'result' && (
          <ResultDisplay
            resultData={resultData}
            onTryAgain={handleTryAgain}
          />
        )}
      </main>
    </div>
  );
}

export default App;
