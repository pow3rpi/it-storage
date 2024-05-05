import { API_URL } from '../../config';

export default async function logInRequest(requestBody) {
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    credentials: 'include',
    body: requestBody,
  };
  return await fetch(`${API_URL}/log_in`, options)
    .then((response) => response.json());
}