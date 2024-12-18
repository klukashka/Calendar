import React, { useState } from 'react';
import {back_host, back_port} from '../config.jsx';

const NoteCreate = () => {
    const [remindTime, setRemindTime] = useState('');
    const [message, setMessage] = useState('');
    const [important, setImportant] = useState(false);
    const [timeZone, setTimeZone] = useState('');

    const handleCheckboxChange = (event) => {
        const { checked } = event.target;
        setImportant(checked);
    };

    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleNoteCreate = async (event) => {

        const localTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        setTimeZone(localTimeZone);

        event.preventDefault();

        const note_to_create = {
        'remind_time': remindTime,
        'message': message,
        'important': important,
        'time_zone': localTimeZone,
        };

        try {
            const response = await fetch(`http://${back_host}:${back_port}/account/note_create`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify(note_to_create)
                });
            if (!response.ok){
                setError('There was a problem with creating a new note.');
            }
            setSuccess('A new note was created successfully');
            console.log('A new note was created successfully:', response);
        } catch(error){
            console.error('There was a problem with creating a new note:', error);
        }
    };

    let main_form = <form onSubmit={handleNoteCreate}>
                      <div>
                          <label>
                            Select date and time:
                            <input
                              type="datetime-local"
                              value={remindTime}
                              onChange={(e) => setRemindTime(e.target.value)}
                            />
                          </label>
                      </div>
                      <div>
                          <label>
                            Write a message:
                            <input
                              type="text"
                              value={message}
                              onChange={(e) => setMessage(e.target.value)}
                            />
                          </label>
                      </div>
                      <div>
                          <label>
                            Is it important?
                            <input
                              type="checkbox"
                              checked={important}
                              onChange={handleCheckboxChange}
                            />
                          </label>
                      </div>
                      <div>
                        <button type="submit" style={{ padding: "10px 15px", fontSize: "16px" }}>Create</button>
                      </div>
                      <br></br>
                    </form>

    if (error) {
        return (
            <div>
                {main_form}
                <div style={{ color: 'red' }}>{error}</div>
            </div>
        )
    }

    if (success){
        return (
            <div>
                {main_form}
                <div style={{ color: 'green' }}>{success}</div>
            </div>
        )
    }

    return main_form
};

export default NoteCreate;