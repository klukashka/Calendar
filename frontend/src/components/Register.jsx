import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';


const Register = () => {
  const navigate = useNavigate();
  const [nickname, setNickname] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');


  const handleSubmit = async (event) => {
    event.preventDefault();

    const data_to_send = {
        'nickname': nickname,
        'email': email,
        'password': password
        };

//     const formData = new FormData();
//     formData.append('email', email);
//     formData.append('password', password);

    try {
      const response = await fetch('http://localhost:8000/auth/register', {
        method: 'POST',
        headers: {
                'Content-Type': 'application/json',
            },
        body: JSON.stringify(data_to_send)
        });

      if (!response.ok) {
        setError('Registration failed');
        throw new Error('Network response was not ok');
      }

      const data = response;

      console.log('You were successfully registered:', data);
      setSuccess('You were successfully registered!');
      navigate('/');
    } catch (error) {
      console.error('There was a problem with the register request:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="nickname">Nickname:</label>
        <input
          type="text"
          id="nickname"
          value={nickname}
          onChange={(e) => setNickname(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit">Register</button>
    </form>
  );
};

export default Register;
