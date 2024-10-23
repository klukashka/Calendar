import React, { useState, useEffect } from 'react';
import {back_host, back_port} from '../config.jsx';

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false };
    const date = new Date(dateString);
    return date.toLocaleString('en-GB', options);
}

const NotesGet = () => {
  const [notes, setNotes] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchNotes = async () => {
      try {
        const response = await fetch(`http://${back_host}:${back_port}/account/notes_get`, {
            method: 'GET',
            credentials: 'include',
        });
        const notes_data = await response.json();
        console.log('Got notes successfully', notes_data);
        console.log('First note', notes_data[0]);
        setNotes(notes_data);
      } catch (error) {
        setError(error.message);
      }
    };

    fetchNotes();
  }, []); // Empty dependency array means this useEffect runs once after the component mounts

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <ul>
        {notes.map((note, index) => (
          <li key={index}>
            <div>
                <p>Message:  </p>
                <strong>
                    {note.message}.
                </strong>
            </div>
            <div>
                <p>When to remind: </p>
                <strong>
                    {formatDate(note.remind_time)}
                </strong>
                <br></br>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default NotesGet;