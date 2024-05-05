import { API_URL } from '../../config';

export default async function updateLinkRequest(id, requestBody) {
  const options = {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: requestBody,
  };
  return await fetch(`${API_URL}/links/${id}`, options)
    .then((response) => response.json());
}