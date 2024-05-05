import { API_URL } from '../../config';

export default async function changePasswordRequest(requestBody) {
  const options = {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: requestBody,
  };
  return await fetch(`${API_URL}/change_password`, options)
    .then((response) => response.json());
}