import React from 'react';
import { useNavigate } from 'react-router-dom';

const Logout = () => {
    const navigate = useNavigate();

    const handleLogout = async (event) => {
        event.preventDefault();

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

    return (
        <button onClick={handleLogout} style={{ padding: "10px 15px", fontSize: "16px" }}>
            Logout
        </button>
    )
};

export default Logout;