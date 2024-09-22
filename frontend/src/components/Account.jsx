import React, { useEffect, useState } from 'react';
import Logout from '../hooks/Logout';
import NoteCreate from '../hooks/NoteCreate';
import NotesGet from '../hooks/NotesGet';

const Account = () => {
    const [user, setUser] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchUser = async () => {
            const response = await fetch('http://localhost:8000/account/user_info', {
                method: 'GET',
                credentials: 'include',
            });

            if (response.ok) {
                const userData = await response.json();
                console.log('Logged in successfully:', userData);
                setUser(userData);
            } else {
                setError('You need to log in to access this page.');
            }
        };

        fetchUser();
    }, []);

    if (error) {
        return <div style={{ color: 'red' }}>{error}</div>;
    }

    if (!user) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>Calendar account</h2>
            <p>Welcome, {user.nickname}!</p>
            <h4>You can create a new note:</h4>
                <NoteCreate />
            <h4>Here are your current notes:</h4>
            <NotesGet />
            <Logout />
        </div>
    );
};

export default Account;