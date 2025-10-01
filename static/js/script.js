document.getElementById("translate-button").addEventListener("click", function(event) {
    event.preventDefault();
    const form = event.target.form;
    const formData = new FormData(form);

    fetch('/translate', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        // Check if the request was successful based on the HTTP status code
        if (!response.ok) {
            // Throw an error that the .catch block can handle
            throw new Error(`Server returned status: ${response.status}`);
        }
        // If successful, proceed to parse the JSON
        return response.json();
    })
    .then(data => {
        // Display the translated text
        document.getElementById("snippet").textContent = data.translation;
    })
    .catch(error => {
        // Display a general error message to the user
        console.error("Fetch Error:", error);
        document.getElementById("snippet").textContent = "Error: Could not complete translation.";
    });
});

let speech = new SpeechSynthesisUtterance()

document.getElementById("pronounce-button").addEventListener("click", function() {
        const textToSpeak = document.getElementById("snippet").textContent;
        // responsiveVoice.speak(textToSpeak, 'UK English Female', { delay: 0 });
        speech.text = textToSpeak
        window.speechSynthesis.speak(speech)
        
    });

function downloadTxtFile() {
        const textContent = document.getElementById('snippet').textContent;
        const filename = 'trad.txt';
        const blob = new Blob([textContent], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a); // Append to the body (can be hidden)
        a.click(); // Programmatically click the link to trigger download

        document.body.removeChild(a); // Clean up the temporary link
        URL.revokeObjectURL(url); // Release the object URL
}