import { json } from "stream/consumers";

export default async function Page(){

    const response = await fetch(process.env.URL + '/api/hello', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

    // const b = await response.text()

    // console.log(b);
    
    // // alert(response.body)
    const value = await response.json();
    console.log(process.env.URL);
    return <div>{JSON.stringify(value)}</div>;
}