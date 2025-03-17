import fs from 'fs';
import path from 'path';
import { NextApiRequest, NextApiResponse } from 'next';

// Define the path to the JSON file
const filePath = path.resolve(process.cwd(), 'data.json');

// Define the expected structure of your data
interface DataItem {
  id: number;
  name: string;
  email: string;
}

// API handler function
export default function handler(req: NextApiRequest, res: NextApiResponse): void {
  if (req.method === 'POST') {
    const { data }: { data: DataItem } = req.body;

    // Read the existing data from the JSON file
    fs.readFile(filePath, 'utf8', (err, fileData) => {
      if (err) {
        res.status(500).json({ error: 'Error reading data file.' });
        return;
      }

      let jsonData: DataItem[] = [];
      if (fileData) {
        try {
          jsonData = JSON.parse(fileData);
        } catch (parseError) {
          res.status(500).json({ error: 'Error parsing JSON file.' });
          return;
        }
      }

      // Append new data
      jsonData.push(data);

      // Write the updated data back to the JSON file
      fs.writeFile(filePath, JSON.stringify(jsonData, null, 2), (writeErr) => {
        if (writeErr) {
          res.status(500).json({ error: 'Error saving data.' });
          return;
        }

        res.status(201).json({ message: 'Data saved successfully!' });
      });
    });
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}