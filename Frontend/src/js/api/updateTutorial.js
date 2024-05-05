import { API_URL } from '../../config';

export default async function updateTutorialRequest(id, requestBody) {
  const options = {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: requestBody,
  };
  return await fetch(`${API_URL}/tutorials/${id}`, options)
    .then((response) => response.json());
}