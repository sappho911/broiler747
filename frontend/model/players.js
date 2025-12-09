export async function getPlayers(){
   const responce = await fetch("http://127.0.0.1:5000/api/players");
   const data = await responce.json();
   return data;
}