var socket = io({
    host: 'localhost',
    port: 5000
});

socket.on('connect', function () {
    console.log('Connected to server');
});

socket.on('sex_with_andrewmama', function (message) {
    console.log("response received");
    console.log(message);

    var messageList = document.getElementById('input_list');
    messageList.innerHTML = ''; // Clear the existing content

    for (var i = 0; i < message.length; i++) {
        var listItem = document.createElement('li');
        listItem.textContent = message[i];
        messageList.appendChild(listItem);
    }
});

document.getElementById('start_snipe_button').addEventListener('click', function () {
    document.getElementById('status_bar').innerHTML = 'Starting Sniper...';
    socket.emit('start_sniper');
    console.log('Starting_sniper')
});
