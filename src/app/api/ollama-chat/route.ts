import { NextResponse } from 'next/server';

const OLLAMA_API_URL = 'http://localhost:11434/api/generate'; // Replace with your Ollama endpoint

export async function POST(req: Request) {
  const { prompt }= await req.json();

  const request = { model: "llama3.2", prompt: prompt, stream: false} 
    try {
      const response = await fetch(OLLAMA_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });
      
      if (!response.ok) {
        NextResponse.json(response.statusText)
        //throw new Error('Failed to communicate with Ollama API.');
      }

      const data = await response.json();
      return NextResponse.json(data);
    } catch (error) {
      console.error('Error:', error);
      return NextResponse.json({ error: 'Error processing request.' });
    }
}

// export default async function POST(req: Request) {
//     const { prompt } = await req.json();

//     // Validate input
//     if (!prompt || typeof prompt !== 'string') {
//       NextResponse.json({ error: 'Invalid input. "prompt" must be a non-empty string.' });
//       return;
//     }

//     try {
//       const response = await fetch(OLLAMA_API_URL, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ prompt }),
//       });

//       if (!response.ok) {
//         throw new Error('Failed to communicate with Ollama API.');
//       }

//       const data = await response.json();
//       NextResponse.json(data);
//     } catch (error) {
//       console.error('Error:', error);
//       NextResponse.json({ error: 'Error processing request.' });
//     }
// }