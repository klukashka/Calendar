// import React, { useEffect, useState } from 'react';
// import { useHistory } from 'react-router-dom';
//
// const Account = () => {
//     const [userData, setUserData] = useState(null);
//     const [loading, setLoading] = useState(true);
//     const history = useHistory();
//
//     useEffect(() => {
//         const token = localStorage.getItem('jwt'); // Replace with your actual storage method
//
//         if (!token) {
//             // No token means the user is not authenticated
//             history.push('/auth/jwt/login'); // Redirect to login page
//             return;
//         }
//
//         // Fetch user data
//         fetch('/', {
//             method: 'GET',
//             headers: {
//                 'Authorization': `JWT ${token}`,
//                 'Content-Type': 'application/json'
//             },
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             setUserData(data);
//             setLoading(false);
//         })
//         .catch(error => {
//             console.error('Error fetching user data:', error);
//             history.push('/auth/jwt/login'); // Redirect to login if there's an error
//         });
//     }, [history]);
//
//     if (loading) {
//         return <div>Loading...</div>; // Show a loading indicator
//     }
//
//     return (
//         <div>
//             <h1>Your Account</h1>
//             {userData ? (
//                 <div>
//                     <h2>Welcome</h2>
//                     <p>Email: {userData.email}</p>
//                     {/* Add more account details as needed */}
//                 </div>
//             ) : (
//                 <p>No user data found.</p>
//             )}
//         </div>
//     );
// };
//
// export default Account;


import React, { useState } from 'react';

const Account = () => {
  const [message, setMessage] = useState("Hello, World!");

  const changeMessage = () => {
    setMessage("You clicked the button!");
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>{message}</h1>
      <button onClick={changeMessage} style={{ padding: "10px 15px", fontSize: "16px" }}>
        Click Me
      </button>
    </div>
  );
};

export default Account;