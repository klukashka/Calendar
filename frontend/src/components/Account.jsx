import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Account = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [error, setError] = useState('');

    const logout = async () => {
        try {
            const response = await fetch('http://localhost:8000/auth/jwt/logout', {
                    method: 'POST',
                    credentials: 'include',
                });
            if (!response.ok){
                throw new Error('Network response was not ok');
            }
            console.log('Logged out successfully:', response);
            navigate('/');
        } catch(error){
            console.error('There was a problem with the logout request:', error);
        }
    };

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
            <p>Welcome, {user.nickname}</p>
            <button onClick={logout} style={{ padding: "10px 15px", fontSize: "16px" }}>
                Logout
            </button>
        </div>
    );
};

export default Account;