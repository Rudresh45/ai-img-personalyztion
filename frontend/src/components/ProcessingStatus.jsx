import { useState, useEffect } from 'react';
import API_BASE_URL from '../config/api';


function ProcessingStatus({ requestId, onComplete, onError }) {
    const [status, setStatus] = useState('processing');
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        let pollInterval;
        let progressInterval;

        // Simulate progress animation
        progressInterval = setInterval(() => {
            setProgress((prev) => {
                if (prev >= 90) return prev;
                return prev + Math.random() * 10;
            });
        }, 500);

        // Poll for result
        const checkStatus = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/result/${requestId}/`);

                if (!response.ok) {
                    throw new Error('Failed to check status');
                }

                const data = await response.json();

                if (data.status === 'completed') {
                    setProgress(100);
                    clearInterval(pollInterval);
                    clearInterval(progressInterval);
                    setTimeout(() => {
                        onComplete(data);
                    }, 500);
                } else if (data.status === 'failed') {
                    clearInterval(pollInterval);
                    clearInterval(progressInterval);
                    onError(data.error_message || 'Processing failed. Please try again.');
                }
            } catch (err) {
                console.error('Status check error:', err);
                clearInterval(pollInterval);
                clearInterval(progressInterval);
                onError('Failed to check processing status. Please try again.');
            }
        };

        // Check immediately
        checkStatus();

        // Then poll every 2 seconds
        pollInterval = setInterval(checkStatus, 2000);

        return () => {
            clearInterval(pollInterval);
            clearInterval(progressInterval);
        };
    }, [requestId, onComplete, onError]);

    return (
        <div className="card">
            <div className="loading">
                <div className="spinner"></div>
                <p className="loading-text">
                    {status === 'processing' ? '🎨 Creating your cartoon illustration...' : 'Processing...'}
                </p>

                <div className="progress-bar">
                    <div
                        className="progress-fill"
                        style={{ width: `${progress}%`, animation: 'none' }}
                    ></div>
                </div>
            </div>
        </div>
    );
}

export default ProcessingStatus;
