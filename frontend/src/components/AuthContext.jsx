// import React, { createContext, useState } from 'react';
//
// export const AuthContext = createContext();
//
// export const AuthProvider = ({ children }) => {
//     const [user, setUser] = useState(null);
//     const [token, setToken] = useState(null);
//
//     const login = (userData, token) => {
//         setUser(userData);
//         setToken(token);
//         localStorage.setItem('token', token); // Save token in local storage
//     };
//
//     const logout = () => {
//         setUser(null);
//         setToken(null);
//         localStorage.removeItem('token'); // Remove token from local storage
//     };
//
//     return (
//         <AuthContext.Provider value={{ user, token, login, logout }}>
//             {children}
//         </AuthContext.Provider>
//     );
// };