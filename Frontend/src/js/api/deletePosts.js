import { API_URL } from '../../config';

export default async function deletePostsRequest(requestBody) {
  const options = {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: requestBody,
  };
  return await fetch(`${API_URL}/posts/`, options)
    .then((response) => response.json());
}