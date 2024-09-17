import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Account from './components/Account'

const App = () => {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/account" element={<Account />} />
        <Route path="/auth/jwt/login" element={<Login />} />
        <Route path="/auth/register" element={<Register />} />
      </Routes>
    </div>
  );
};

const Home = () => {
  return (
    <div style={{ maxWidth: '400px', margin: 'auto' }}>
      <h1>Calendar</h1>
      <Link to="/auth/jwt/login">
        <button>Login</button>
      </Link>
      <Link to="/auth/register">
        <button>Register</button>
      </Link>
    </div>
  );
};

export default App;
