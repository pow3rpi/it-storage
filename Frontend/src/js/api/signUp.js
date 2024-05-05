import { API_URL } from '../../config';

export default async function signUpRequest(requestBody) {
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: requestBody,
  };
  return await fetch(`${API_URL}/sign_up`, options)
    .then(response => response.json());
}