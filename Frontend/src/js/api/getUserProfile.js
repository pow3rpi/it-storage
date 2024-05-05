import { API_URL } from '../../config';

export default async function getUserProfileRequest() {
  const options = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include',
  };
  return await fetch(`${API_URL}/get_me`, options)
    .then((response) => response.json());
}