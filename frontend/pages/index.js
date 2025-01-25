import React, { useState } from 'react';
import { useRouter } from 'next/router';

const Home = () => {
    const [apiKey, setApiKey] = useState('');
    const [pdfFile, setPdfFile] = useState(null);
    const [invalidApiKeyError, setInvalidApiKeyError] = useState('');
    const router = useRouter();

    const handleFileChange = (e) => {
        setPdfFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('pdf', pdfFile);
        formData.append('apiKey', apiKey);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();

            if (response.status === 400) {
                if (data.error === "Invalid API key") {
                    setInvalidApiKeyError(data.error);
                } else {
                    alert(data.error);
                }
                return;
            }

            if (data.text_found) {
                router.push({
                    pathname: '/chat',
                    query: { apiKey },
                });
            } else {
                router.push({
                    pathname: '/no-text',
                    query: { metadata: JSON.stringify(data.metadata) },
                });
            }
        } catch (error) {
            console.error('Upload error:', error);
            alert('An unexpected error occurred');
        }
    };

    const handleGoBack = () => {
        setInvalidApiKeyError('');
    };

    return (
        <div>
            <h1>Upload PDF and Enter API Key</h1>
            {invalidApiKeyError ? (
                <div>
                    <p className="error-text">{invalidApiKeyError}</p>
                    <button onClick={handleGoBack}>Go Back to Home</button>
                </div>
            ) : (
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Enter Mistral AI API Key"
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                        required
                    />
                    <p style={{ fontSize: '0.8em' }}>Don't have an API key? Get one from <a href="https://console.mistral.ai/api-keys/" target="_blank" rel="noopener noreferrer">Mistral AI Console</a></p>
                    <input type="file" onChange={handleFileChange} required />
                    <button type="submit">Submit</button>
                </form>
            )}
        </div>
    );
};

export default Home;