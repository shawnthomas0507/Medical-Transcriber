import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Mic, MicOff } from "lucide-react";

export default function MedicalTranscriber() {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState("");

  const toggleRecording = async () => {
    if (isRecording) {
      // Stop recording logic
      setIsRecording(false);
    } else {
      // Start recording logic
      setIsRecording(true);
      setTranscript("Listening...");
      
      // Call backend API to process speech
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold mb-4">Medical AI Transcriber</h1>
      <Button
        onClick={toggleRecording}
        className="p-6 bg-blue-500 text-white rounded-full shadow-lg transition-transform transform hover:scale-110"
      >
        {isRecording ? <MicOff size={32} /> : <Mic size={32} />}
      </Button>
      <p className="mt-4 text-lg text-gray-700">{transcript}</p>
    </div>
  );
}
