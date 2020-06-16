const io = require("socket.io");
const server = io.listen(3000);
const nicknames = {}

server.on('connection', (socket) => {
    console.log('connected');
    socket.on('message', (message) => {
        server.emit('message', nicknames[socket.id], message);
    });

    socket.on('login', (nickname) => {
        nicknames[socket.id] = nickname;
        socket.emit('login', true);
        server.emit('user', nickname);
        server.emit('newuser', nickname);
    });

    socket.on('disconnect', () => {
        const nickname = nicknames[socket.id];
        delete nicknames[socket.id];
        server.emit('disconnect', nickname);
        server.emit('users', Object.values(nicknames));
    });
});