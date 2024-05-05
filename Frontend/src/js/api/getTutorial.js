import { API_URL } from '../../config';

export default async function getTutorial(id) {
  const options = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include'
  };
  return await fetch(`${API_URL}/tutorials/${id}`, options)
    .then((response) => response.json());
}