import { API_URL } from '../../config';

export default async function getTags(string) {
  const options = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include'
  };
  const searchParam = new URLSearchParams({ string: string });
  return await fetch(`${API_URL}/posts/tags?${searchParam}`, options)
    .then((response) => response.json());
}