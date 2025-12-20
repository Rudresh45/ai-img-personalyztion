import { useState, useRef } from 'react';
import API_BASE_URL from '../config/api';


function UploadForm({ onUploadComplete, error }) {
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const fileInputRef = useRef(null);

    const handleFileSelect = (file) => {
        if (file && file.type.startsWith('image/')) {
            setSelectedFile(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setPreviewUrl(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleFileInputChange = (e) => {
        const file = e.target.files[0];
        handleFileSelect(file);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const file = e.dataTransfer.files[0];
        handleFileSelect(file);
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        setIsUploading(true);

        try {
            // Step 1: Upload the photo
            const formData = new FormData();
            formData.append('uploaded_photo', selectedFile);

            const uploadResponse = await fetch(`${API_BASE_URL}/upload/`, {
                method: 'POST',
                body: formData,
            });

            if (!uploadResponse.ok) {
                // Try to get error message from response
                let errorMessage = 'Upload failed';
                try {
                    const errorData = await uploadResponse.json();
                    console.error('Upload error response:', errorData);
                    errorMessage = errorData.error || errorData.uploaded_photo?.[0] || errorMessage;
                } catch (e) {
                    console.error('Failed to parse error response:', e);
                }
                throw new Error(errorMessage);
            }

            const uploadData = await uploadResponse.json();
            const requestId = uploadData.id;

            // Step 2: Trigger processing
            const processResponse = await fetch(`${API_BASE_URL}/process/${requestId}/`, {
                method: 'POST',
            });

            if (!processResponse.ok) {
                const errorData = await processResponse.json();
                console.error('Process error response:', errorData);
                throw new Error(errorData.error || 'Failed to start processing');
            }

            // Notify parent component
            onUploadComplete(requestId);
        } catch (err) {
            console.error('Upload error:', err);

            // Provide specific error messages
            let userMessage = 'Failed to upload photo. Please try again.';

            if (err.message.includes('Failed to fetch') || err.name === 'TypeError') {
                userMessage = 'Cannot connect to server. Please check if the backend is running.';
            } else if (err.message !== 'Upload failed' && err.message !== 'Failed to start processing') {
                userMessage = err.message;
            }

            alert(userMessage);
        } finally {
            setIsUploading(false);
        }
    };

    const handleReset = () => {
        setSelectedFile(null);
        setPreviewUrl(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    return (
        <div className="card">
            {error && (
                <div className="status-message status-error">
                    <span>⚠️</span>
                    <span>{error}</span>
                </div>
            )}

            {!previewUrl ? (
                <div
                    className={`upload-zone ${isDragging ? 'drag-over' : ''}`}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                >
                    <div className="upload-icon">📸</div>
                    <p className="upload-text">
                        <strong>Click to upload</strong> or drag and drop
                    </p>
                    <p className="upload-hint">
                        PNG, JPG
                    </p>
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept="image/*"
                        onChange={handleFileInputChange}
                    />
                </div>
            ) : (
                <div className="image-preview">
                    <img
                        src={previewUrl}
                        alt="Preview"
                        className="preview-image"
                    />
                    <div className="preview-actions">
                        <button
                            className="btn btn-primary btn-full"
                            onClick={handleUpload}
                            disabled={isUploading}
                        >
                            {isUploading ? 'Uploading...' : '✨ Personalize Photo'}
                        </button>
                        <button
                            className="btn btn-secondary btn-full"
                            onClick={handleReset}
                            disabled={isUploading}
                        >
                            Choose Different Photo
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default UploadForm;
