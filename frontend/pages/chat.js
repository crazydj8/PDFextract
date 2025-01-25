import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

const Chat = () => {
    const router = useRouter();
    const { apiKey } = router.query;
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [showOverlay, setShowOverlay] = useState(false);
    const [overlayContent, setOverlayContent] = useState('');
    const [extractedText, setExtractedText] = useState({});
    const [metadata, setMetadata] = useState({});
    const [selectedPage, setSelectedPage] = useState('');
    const [rateLimitError, setRateLimitError] = useState('');

    useEffect(() => {
        if (!apiKey) {
            router.push('/');
        }
    }, [apiKey]);

    const handleQuestionSubmit = async (e) => {
        e.preventDefault();
        setRateLimitError(''); // Clear previous error message
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }),
        });
    
        const data = await response.json();
        if (response.status === 429) {
            setRateLimitError("Error 429, you have been rate limited, try after a few seconds");
            return;
        }
    
        setAnswer(data.answer);
    };

    const handleGoBack = () => {
        router.push('/');
    };

    const handleShowOverlay = async (type) => {
        if (type === 'text') {
            const response = await fetch('/api/extracted_text', {
                method: 'GET',
            });
            const data = await response.json();
            setExtractedText(data.extracted_text);
            setOverlayContent('text');
        } else if (type === 'metadata') {
            const response = await fetch('/api/metadata', {
                method: 'GET',
            });
            const data = await response.json();
            setMetadata(data.metadata);
            setOverlayContent('metadata');
        }
        setShowOverlay(true);
    };

    const handleCloseOverlay = () => {
        setShowOverlay(false);
        setOverlayContent('');
    };

    const handlePageChange = (e) => {
        setSelectedPage(e.target.value);
    };

    return (
        <div>
            <h1>Chat with Extracted Text</h1>
            <form onSubmit={handleQuestionSubmit}>
                <input
                    type="text"
                    placeholder="Ask a question"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    required
                />
                {rateLimitError && <p className="error-text">{rateLimitError}</p>}
                <button type="submit" className="ask-button">Ask</button>
            </form>
            {answer && <p>Answer: {answer}</p>}
            <button onClick={() => handleShowOverlay('text')}>Show Extracted Text</button>
            <button onClick={() => handleShowOverlay('metadata')}>Show Metadata</button>
            <button className="gobackbutton" onClick={handleGoBack}>Go Back to Home</button>

            {showOverlay && (
                <div className="overlay">
                    <button onClick={handleCloseOverlay}>Close</button>
                    {overlayContent === 'text' && (
                        <div className="content">
                            <h2>Extracted Text</h2>
                            <select onChange={handlePageChange}>
                                <option value="">Select a page</option>
                                {Object.keys(extractedText).map((page) => (
                                    <option key={page} value={page}>
                                        Page {page}
                                    </option>
                                ))}
                            </select>
                            {selectedPage && <p>{extractedText[selectedPage]}</p>}
                        </div>
                    )}
                    {overlayContent === 'metadata' && (
                        <div className="content">
                            <h2>Metadata</h2>
                            <pre>{JSON.stringify(metadata, null, 2)}</pre>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Chat;