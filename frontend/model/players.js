export async function getPlayers(){
   const responce = await fetch("/api/players");
   const data = await responce.json();
   return data;
}