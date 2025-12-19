const API_BASE_URL = 'http://localhost:8000';

function ResultDisplay({ resultData, onTryAgain }) {
    const resultImageUrl = resultData.result_image
        ? `${API_BASE_URL}${resultData.result_image}`
        : null;

    const handleDownload = () => {
        if (resultImageUrl) {
            const link = document.createElement('a');
            link.href = resultImageUrl;
            link.download = `personalized-photo-${resultData.id}.jpg`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    };

    return (
        <div className="card">
            <div className="result-container">
                <div className="status-message status-success">
                    <span>✅</span>
                    <span>Your personalized cartoon  illustration is ready!</span>
                </div>

                {resultImageUrl && (
                    <div style={{ marginTop: '1.5rem' }}>
                        <img
                            src={resultImageUrl}
                            alt="Personalized Result"
                            className="result-image"
                        />
                    </div>
                )}

                {resultData.face_confidence && (
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1rem' }}>
                        Face detection confidence: {(resultData.face_confidence * 100).toFixed(1)}%
                    </p>
                )}

                <div className="result-actions">
                    <button className="btn btn-primary" onClick={handleDownload}>
                        📥 Download Image
                    </button>
                    <button className="btn btn-secondary" onClick={onTryAgain}>
                        🔄 Try Another Photo
                    </button>
                </div>
            </div>
        </div>
    );
}

export default ResultDisplay;
