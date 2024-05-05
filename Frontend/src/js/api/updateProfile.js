import { API_URL } from '../../config';

export default async function updateProfileRequest(requestBody) {
  const options = {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: requestBody,
  };
  return await fetch(`${API_URL}/update_profile`, options)
    .then((response) => response.json());
}