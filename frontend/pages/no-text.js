import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

const NoText = () => {
    const router = useRouter();
    const [metadata, setMetadata] = useState(null);

    useEffect(() => {
        if (router.query.metadata) {
            try {
                setMetadata(JSON.parse(router.query.metadata));
            } catch (error) {
                console.error('Failed to parse metadata:', error);
                router.push('/');
            }
        } else {
            router.push('/');
        }
    }, [router.query.metadata]);

    const handleGoBack = () => {
        router.push('/');
    };

    if (!metadata) {
        return null; // or a loading spinner
    }

    return (
        <div>
            <h1>No Text Found in PDF</h1>
            <h2>Metadata:</h2>
            <pre>{JSON.stringify(metadata, null, 2)}</pre>
            <button onClick={handleGoBack}>Go Back</button>
        </div>
    );
};

export default NoText;