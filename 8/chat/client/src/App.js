import React, {useState, useEffect} from "react";
import io from "socket.io-client";
import Input from "./Components/Input"

const socket = io("http://localhost:3000");
export default function App() {
    const [messages, setMessages] = useState([]);
    const [loggedIn, setLoggedIn] = useState(false);
    const [users, setUsers] = useState([])

    useEffect(() => {
        socket.on('message', (nick, message) => {
            setMessages(m => [...m, nick + ": " + message]);
        });
        socket.on('login', loggedIn => {
            setLoggedIn(loggedIn);
        });
        socket.on('users', users => {
            setUsers(u => [...u, users])
        });
        socket.on('newuser', (nick) => {
            setMessages(m => [...m, nick + " joined"])
            setUsers(u => [...u, nick])
        })
        socket.on('disconnect', nick => {
            setMessages(m => [...m, nick + " leaves"])
            setUsers(u => []);
        });
    }, []);
    const send = (message) => {
        socket.emit('message', message);
    }

    const login = (nickname) => {
        socket.emit('login', nickname);
    }

    if (!loggedIn) {
        return (
            <div>
                <h2>Nickname:</h2>
                <Input send={login}/>
            </div>
        )
    } else {
        return (
            <div>
                <h2>Logged-in users</h2>
                <ul>
                    {users.map(u => <li>{u}</li>)}
                </ul>
                <h2>Chatbox</h2>
                <ul>
                    {messages.map(m => <li>{m}</li>)}
                    <Input send={send}/>
                </ul>
            </div>
        )
    }
}