import { useState, useRef } from 'react';

const API_BASE_URL = 'http://localhost:8000/api';

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
                throw new Error('Upload failed');
            }

            const uploadData = await uploadResponse.json();
            const requestId = uploadData.id;

            // Step 2: Trigger processing
            const processResponse = await fetch(`${API_BASE_URL}/process/${requestId}/`, {
                method: 'POST',
            });

            if (!processResponse.ok) {
                throw new Error('Failed to start processing');
            }

            // Notify parent component
            onUploadComplete(requestId);
        } catch (err) {
            console.error('Upload error:', err);
            alert('Failed to upload photo. Please try again.');
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
