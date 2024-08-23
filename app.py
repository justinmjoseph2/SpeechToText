import streamlit as st

# Add custom CSS styling
st.markdown("""
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
            background-color: #f8f9fa;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .container {
            width: 80%;
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }
        h1 {
            color: #007bff;
            margin-bottom: 30px;
        }
        .textarea-container {
            width: 100%;
            height: 300px;
            margin-bottom: 30px;
        }
        textarea {
            width: 100%;
            height: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #fff;
            color: #333;
            resize: none;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            font-size: 16px;
            font-family: Arial, sans-serif;
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        .button {
            padding: 12px 24px;
            font-size: 16px;
            cursor: pointer;
            border: none;
            border-radius: 5px;
            background-color: #007bff;
            color: #fff;
            transition: background-color 0.3s, box-shadow 0.3s;
            height: 50px;
            line-height: 50px;
            display: inline-flex;
            align-items: center;
            font-weight: bold;
        }
        .button:hover {
            background-color: #0056b3;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .button:active {
            background-color: #004494;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .download-button {
            background-color: #28a745;
        }
        .download-button:hover {
            background-color: #218838;
        }
        .download-button:active {
            background-color: #1e7e34;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Real-Time Speech to Text Converter with Voice Segmentation")

# Container for the UI elements
st.markdown('<div class="container">', unsafe_allow_html=True)

# Add custom HTML for text area and buttons
st.components.v1.html("""
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: rgb(14, 17, 23);
            color: #333;
            text-align: center;
            padding: 20px;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        .button-container {
            display: flex;
            justify-content: center; /* Center buttons horizontally */
            gap: 20px; /* Space between buttons */
            margin-top: 20px;
        }
        button {
            padding: 10px 20px;
            font-size: 18px;
            cursor: pointer;
            border: none;
            border-radius: 5px;
            background-color: #007bff;
            color: #fff;
            transition: background-color 0.3s;
            height: 50px; /* Set a consistent height for both buttons */
            line-height: 50px; /* Center text vertically */
            display: inline-flex; /* Align icon and text horizontally */
            align-items: center; /* Center text and icon vertically */
            font-weight: bold; /* Make text bold */
        }
        button i {
            margin-right: 10px; /* Space between icon and text */
            font-size: 24px; /* Icon size */
        }
        button:hover {
            background-color: #0056b3;
        }
        textarea {
            width: 100%;
            height: 200px;
            padding: 15px;
            border: 1px solid #ddd;
            background-color: #fff;
            color: #333;
            resize: none;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            font-size: 18px; /* Larger, more readable font size */
            font-family: 'Georgia', serif; /* Professional, readable font */
            line-height: 1.5; /* Improve readability */
            font-weight: 400; /* Normal weight for better readability */
            overflow-y: auto; /* Enable vertical scrolling */
        }
        #uploadContainer {
            margin-top: 20px;
        }
        #uploadInput {
            display: block;
            margin: 20px auto;
        }
    </style>
    <div class="textarea-container">
        <textarea id="transcript" placeholder="Your transcription will appear here..."></textarea>
    </div>
    <div class="button-container">
        <button id="start_stop_button" class="button" onclick="toggleRecognition()">Start Recording</button>
        <button class="button download-button" onclick="downloadText()">Download as .txt</button>
    </div>

    <script>
        var recognition;
        var isRecording = false;
        var final_transcript = '';
        var segments = [];

        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';

            recognition.onresult = function(event) {
                var interim_transcript = '';
                var segment_text = '';

                for (var i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        segment_text += addPunctuation(event.results[i][0].transcript);
                    } else {
                        interim_transcript += event.results[i][0].transcript;
                    }
                }

                if (segment_text) {
                    segments.push(segment_text);
                }

                document.getElementById('transcript').value = segments.join(' ') + ' ' + interim_transcript;
            };

            recognition.start();
            isRecording = true;
            document.getElementById('start_stop_button').innerHTML = "Stop Recording";
        }

        function stopRecognition() {
            recognition.stop();
            isRecording = false;
            document.getElementById('start_stop_button').innerHTML = "Start Recording";
        }

        function toggleRecognition() {
            if (isRecording) {
                stopRecognition();
            } else {
                startRecognition();
            }
        }

        function addPunctuation(transcript) {
            // Example rule to add punctuation based on basic cues
            // This is very simplistic; for advanced punctuation prediction, you might need a more complex NLP model
            let trimmed = transcript.trim();

            // Add a period if the segment is longer and ends in a complete thought
            if (trimmed.length > 3 && !trimmed.endsWith('.') && !trimmed.endsWith(',')) {
                return trimmed + '. ';
            }
            
            return trimmed + ' ';
        }

        function downloadText() {
            var transcriptArea = document.getElementById('transcript').value;
            var blob = new Blob([transcriptArea], { type: 'text/plain' });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'transcription.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    </script>
""", height=350)

st.markdown('</div>', unsafe_allow_html=True)
