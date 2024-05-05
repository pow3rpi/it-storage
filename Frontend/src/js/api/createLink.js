import { API_URL } from '../../config';

export default async function createLinkRequest(requestBody) {
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: requestBody,
  };
  return await fetch(`${API_URL}/links/create`, options)
    .then((response) => response.json());
}