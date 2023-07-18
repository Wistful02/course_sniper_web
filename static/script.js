var socket = io({
    host: 'localhost',
    port: 5000
});

var textArray = [];

function createDeleteHandler(text) {
    return function () {
        textArray.push(text);
        this.parentNode.remove();
        console.log(textArray);
    };
}

socket.on('connect', function () {
    console.log('Connected to server');
});

socket.on('sex_with_andrewmama', function (message) {
    console.log("response received");

    var messageList = document.getElementById('input_list');
    messageList.innerHTML = ''; // Clear the existing content

    for (var i = 0; i < message.length; i++) {
        var text = message[i] + " is open!";

        if (!textArray.includes(text)) {
            var listItem = document.createElement('li');
            listItem.textContent = text;

            var deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.classList.add('delete-button');
            deleteButton.addEventListener('click', createDeleteHandler(text));

            listItem.appendChild(deleteButton);
            messageList.appendChild(listItem);
        }
    }
    console.log(textArray)
});

socket.on('sniper_started',function () {
    var output = "Sniping";
    document.getElementById('status_bar').innerHTML = output;
});

document.getElementById('start_snipe_button').addEventListener('click', function () {
    document.getElementById('status_bar').innerHTML = 'Starting Sniper... (This might take a while depending on the device you are using)';
    socket.emit('start_sniper');
    console.log('Starting_sniper')
});