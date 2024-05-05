import { API_URL } from '../../config';

export default async function getPostsRequest(params) {
  const options = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include'
  };
  const searchParams = new URLSearchParams(params);
  return await fetch(`${API_URL}/posts?${searchParams}`, options)
    .then((response) => response.json());
}